# Copyright (c) 2020, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import saashq
from saashq.model.document import Document


class UAEVATSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.regional.doctype.uae_vat_account.uae_vat_account import UAEVATAccount

		company: DF.Link
		uae_vat_accounts: DF.Table[UAEVATAccount]
	# end: auto-generated types

	pass
