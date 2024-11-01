# Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from saashq.model.document import Document


class ProjectsSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		ignore_employee_time_overlap: DF.Check
		ignore_user_time_overlap: DF.Check
		ignore_workstation_time_overlap: DF.Check
	# end: auto-generated types

	pass
