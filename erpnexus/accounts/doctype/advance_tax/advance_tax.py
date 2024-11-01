# Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import saashq
from saashq.model.document import Document


class AdvanceTax(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		account_head: DF.Link | None
		allocated_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reference_detail: DF.Data | None
		reference_name: DF.DynamicLink | None
		reference_type: DF.Link | None
	# end: auto-generated types

	pass
