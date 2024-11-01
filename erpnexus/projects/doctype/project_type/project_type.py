# Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.model.document import Document


class ProjectType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		description: DF.Text | None
		project_type: DF.Data
	# end: auto-generated types

	def on_trash(self):
		if self.name == "External":
			saashq.throw(_("You cannot delete Project Type 'External'"))
