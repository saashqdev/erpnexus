# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import saashq
from saashq.model.document import Document


class JobCardScheduledTime(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from_time: DF.Datetime | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		time_in_mins: DF.Float
		to_time: DF.Datetime | None
	# end: auto-generated types

	pass
