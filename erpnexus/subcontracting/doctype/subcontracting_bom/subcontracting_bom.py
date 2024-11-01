# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import saashq
from saashq import _
from saashq.model.document import Document
from saashq.utils import flt


class SubcontractingBOM(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		conversion_factor: DF.Float
		finished_good: DF.Link
		finished_good_bom: DF.Link
		finished_good_qty: DF.Float
		finished_good_uom: DF.Link | None
		is_active: DF.Check
		service_item: DF.Link
		service_item_qty: DF.Float
		service_item_uom: DF.Link
	# end: auto-generated types

	def validate(self):
		self.validate_finished_good()
		self.validate_service_item()
		self.validate_is_active()

	def before_save(self):
		self.set_conversion_factor()

	def validate_finished_good(self):
		disabled, is_stock_item, default_bom, is_sub_contracted_item = saashq.db.get_value(
			"Item",
			self.finished_good,
			["disabled", "is_stock_item", "default_bom", "is_sub_contracted_item"],
		)

		if disabled:
			saashq.throw(_("Finished Good {0} is disabled.").format(saashq.bold(self.finished_good)))
		if not is_stock_item:
			saashq.throw(_("Finished Good {0} must be a stock item.").format(saashq.bold(self.finished_good)))
		if not default_bom:
			saashq.throw(
				_("Finished Good {0} does not have a default BOM.").format(saashq.bold(self.finished_good))
			)
		if not is_sub_contracted_item:
			saashq.throw(
				_("Finished Good {0} must be a sub-contracted item.").format(saashq.bold(self.finished_good))
			)

	def validate_service_item(self):
		disabled, is_stock_item = saashq.db.get_value(
			"Item", self.service_item, ["disabled", "is_stock_item"]
		)

		if disabled:
			saashq.throw(_("Service Item {0} is disabled.").format(saashq.bold(self.service_item)))
		if is_stock_item:
			saashq.throw(
				_("Service Item {0} must be a non-stock item.").format(saashq.bold(self.service_item))
			)

	def validate_is_active(self):
		if self.is_active:
			if sb := saashq.db.exists(
				"Subcontracting BOM",
				{"finished_good": self.finished_good, "is_active": 1, "name": ["!=", self.name]},
			):
				saashq.throw(
					_("There is already an active Subcontracting BOM {0} for the Finished Good {1}.").format(
						saashq.bold(sb), saashq.bold(self.finished_good)
					)
				)

	def set_conversion_factor(self):
		self.conversion_factor = flt(self.service_item_qty) / flt(self.finished_good_qty)


@saashq.whitelist()
def get_subcontracting_boms_for_finished_goods(fg_items: str | list) -> dict:
	if fg_items:
		filters = {"is_active": 1}

		if isinstance(fg_items, list):
			filters["finished_good"] = ["in", fg_items]
		else:
			filters["finished_good"] = fg_items

		if subcontracting_boms := saashq.get_all("Subcontracting BOM", filters=filters, fields=["*"]):
			if isinstance(fg_items, list):
				return {d.finished_good: d for d in subcontracting_boms}
			else:
				return subcontracting_boms[0]

	return saashq._dict({})


@saashq.whitelist()
def get_subcontracting_boms_for_service_item(service_item: str) -> dict:
	if service_item:
		filters = {"is_active": 1, "service_item": service_item}
		Subcontracting_boms = saashq.db.get_all("Subcontracting BOM", filters=filters, fields=["*"])

		if Subcontracting_boms:
			return {d.finished_good: d for d in Subcontracting_boms}

	return {}
