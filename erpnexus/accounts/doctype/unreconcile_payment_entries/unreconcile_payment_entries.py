# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import saashq
from saashq.model.document import Document


class UnreconcilePaymentEntries(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		account: DF.Data | None
		account_currency: DF.Link | None
		allocated_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		party: DF.Data | None
		party_type: DF.Data | None
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		unlinked: DF.Check
	# end: auto-generated types

	pass
