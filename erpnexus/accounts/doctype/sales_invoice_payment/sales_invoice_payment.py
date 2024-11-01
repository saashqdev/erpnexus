# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from saashq.model.document import Document


class SalesInvoicePayment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		account: DF.Link | None
		amount: DF.Currency
		base_amount: DF.Currency
		clearance_date: DF.Date | None
		default: DF.Check
		mode_of_payment: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reference_no: DF.Data | None
		type: DF.ReadOnly | None
	# end: auto-generated types

	pass
