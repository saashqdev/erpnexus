# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.model.document import Document

from erpnexus.stock.utils import get_stock_balance, get_stock_value_on


class QuickStockBalance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		date: DF.Date
		item: DF.Link
		item_barcode: DF.Data | None
		item_description: DF.SmallText | None
		item_name: DF.Data | None
		qty: DF.Float
		value: DF.Currency
		warehouse: DF.Link
	# end: auto-generated types

	pass


@saashq.whitelist()
def get_stock_item_details(warehouse, date, item=None, barcode=None):
	out = {}
	if barcode:
		out["item"] = saashq.db.get_value("Item Barcode", filters={"barcode": barcode}, fieldname=["parent"])
		if not out["item"]:
			saashq.throw(_("Invalid Barcode. There is no Item attached to this barcode."))
	else:
		out["item"] = item

	barcodes = saashq.db.get_values("Item Barcode", filters={"parent": out["item"]}, fieldname=["barcode"])

	out["barcodes"] = [x[0] for x in barcodes]
	out["qty"] = get_stock_balance(out["item"], warehouse, date)
	out["value"] = get_stock_value_on(warehouse, date, out["item"])
	out["image"] = saashq.db.get_value("Item", filters={"name": out["item"]}, fieldname=["image"])
	return out
