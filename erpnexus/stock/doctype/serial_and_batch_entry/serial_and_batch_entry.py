# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import saashq
from saashq.model.document import Document


class SerialandBatchEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		batch_no: DF.Link | None
		delivered_qty: DF.Float
		incoming_rate: DF.Float
		is_outward: DF.Check
		outgoing_rate: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		serial_no: DF.Link | None
		stock_queue: DF.SmallText | None
		stock_value_difference: DF.Float
		warehouse: DF.Link | None
	# end: auto-generated types

	pass
