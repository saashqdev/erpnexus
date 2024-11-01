# Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import saashq
from saashq.model.document import Document


class QualityInspectionParameterGroup(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		group_name: DF.Data
	# end: auto-generated types

	pass
