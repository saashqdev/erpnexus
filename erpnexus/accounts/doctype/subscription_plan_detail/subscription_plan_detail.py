# Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from saashq.model.document import Document


class SubscriptionPlanDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		plan: DF.Link
		qty: DF.Int
	# end: auto-generated types

	pass
