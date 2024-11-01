# Copyright (c) 2013, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.query_builder.functions import Floor, Sum
from saashq.utils import cint
from pypika.terms import ExistsCriterion


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns()
	data = get_bom_stock(filters)

	return columns, data


def get_columns():
	"""return columns"""
	columns = [
		_("Item") + ":Link/Item:150",
		_("Description") + "::300",
		_("BOM Qty") + ":Float:160",
		_("BOM UoM") + "::160",
		_("Required Qty") + ":Float:120",
		_("In Stock Qty") + ":Float:120",
		_("Enough Parts to Build") + ":Float:200",
	]

	return columns


def get_bom_stock(filters):
	qty_to_produce = filters.get("qty_to_produce")
	if cint(qty_to_produce) <= 0:
		saashq.throw(_("Quantity to Produce should be greater than zero."))

	if filters.get("show_exploded_view"):
		bom_item_table = "BOM Explosion Item"
	else:
		bom_item_table = "BOM Item"

	warehouse_details = saashq.db.get_value("Warehouse", filters.get("warehouse"), ["lft", "rgt"], as_dict=1)

	BOM = saashq.qb.DocType("BOM")
	BOM_ITEM = saashq.qb.DocType(bom_item_table)
	BIN = saashq.qb.DocType("Bin")
	WH = saashq.qb.DocType("Warehouse")
	CONDITIONS = ()

	if warehouse_details:
		CONDITIONS = ExistsCriterion(
			saashq.qb.from_(WH)
			.select(WH.name)
			.where(
				(WH.lft >= warehouse_details.lft)
				& (WH.rgt <= warehouse_details.rgt)
				& (BIN.warehouse == WH.name)
			)
		)
	else:
		CONDITIONS = BIN.warehouse == filters.get("warehouse")

	QUERY = (
		saashq.qb.from_(BOM)
		.inner_join(BOM_ITEM)
		.on(BOM.name == BOM_ITEM.parent)
		.left_join(BIN)
		.on((BOM_ITEM.item_code == BIN.item_code) & (CONDITIONS))
		.select(
			BOM_ITEM.item_code,
			BOM_ITEM.description,
			BOM_ITEM.stock_qty,
			BOM_ITEM.stock_uom,
			BOM_ITEM.stock_qty * qty_to_produce / BOM.quantity,
			Sum(BIN.actual_qty).as_("actual_qty"),
			Sum(Floor(BIN.actual_qty / (BOM_ITEM.stock_qty * qty_to_produce / BOM.quantity))),
		)
		.where((BOM_ITEM.parent == filters.get("bom")) & (BOM_ITEM.parenttype == "BOM"))
		.groupby(BOM_ITEM.item_code)
	)

	return QUERY.run()
