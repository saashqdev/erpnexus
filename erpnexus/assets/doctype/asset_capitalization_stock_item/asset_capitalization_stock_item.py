# Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import saashq
from saashq.model.document import Document


class AssetCapitalizationStockItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		actual_qty: DF.Float
		amount: DF.Currency
		batch_no: DF.Link | None
		cost_center: DF.Link | None
		item_code: DF.Link
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		serial_and_batch_bundle: DF.Link | None
		serial_no: DF.Text | None
		stock_qty: DF.Float
		stock_uom: DF.Link
		use_serial_batch_fields: DF.Check
		valuation_rate: DF.Currency
		warehouse: DF.Link
	# end: auto-generated types

	pass
