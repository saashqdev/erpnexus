# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import saashq
from saashq.query_builder.functions import Sum


def execute():
	ps = saashq.qb.DocType("Packing Slip")
	dn = saashq.qb.DocType("Delivery Note")
	ps_item = saashq.qb.DocType("Packing Slip Item")

	ps_details = (
		saashq.qb.from_(ps)
		.join(ps_item)
		.on(ps.name == ps_item.parent)
		.join(dn)
		.on(ps.delivery_note == dn.name)
		.select(
			dn.name.as_("delivery_note"),
			ps_item.item_code.as_("item_code"),
			Sum(ps_item.qty).as_("packed_qty"),
		)
		.where((ps.docstatus == 1) & (dn.docstatus == 0))
		.groupby(dn.name, ps_item.item_code)
	).run(as_dict=True)

	if ps_details:
		dn_list = set()
		item_code_list = set()
		for ps_detail in ps_details:
			dn_list.add(ps_detail.delivery_note)
			item_code_list.add(ps_detail.item_code)

		dn_item = saashq.qb.DocType("Delivery Note Item")
		dn_item_query = (
			saashq.qb.from_(dn_item)
			.select(
				dn.parent.as_("delivery_note"),
				dn_item.name,
				dn_item.item_code,
				dn_item.qty,
			)
			.where((dn_item.parent.isin(dn_list)) & (dn_item.item_code.isin(item_code_list)))
		)

		dn_details = saashq._dict()
		for r in dn_item_query.run(as_dict=True):
			dn_details.setdefault((r.delivery_note, r.item_code), saashq._dict()).setdefault(r.name, r.qty)

		for ps_detail in ps_details:
			dn_items = dn_details.get((ps_detail.delivery_note, ps_detail.item_code))

			if dn_items:
				remaining_qty = ps_detail.packed_qty
				for name, qty in dn_items.items():
					if remaining_qty > 0:
						row_packed_qty = min(qty, remaining_qty)
						saashq.db.set_value("Delivery Note Item", name, "packed_qty", row_packed_qty)
						remaining_qty -= row_packed_qty
