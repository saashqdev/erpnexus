# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from saashq.model.document import Document


class ActivityType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		activity_type: DF.Data
		billing_rate: DF.Currency
		costing_rate: DF.Currency
		disabled: DF.Check
	# end: auto-generated types

	pass
