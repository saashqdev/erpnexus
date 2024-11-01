# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import saashq
from saashq.model.document import Document


class QualityFeedbackParameter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		feedback: DF.TextEditor | None
		parameter: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		rating: DF.Literal["", "1", "2", "3", "4", "5"]
	# end: auto-generated types

	pass
