# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from saashq.model.document import Document


class PricingRuleDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		child_docname: DF.Data | None
		item_code: DF.Data | None
		margin_type: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		pricing_rule: DF.Link | None
		rate_or_discount: DF.Data | None
		rule_applied: DF.Check
	# end: auto-generated types

	pass
