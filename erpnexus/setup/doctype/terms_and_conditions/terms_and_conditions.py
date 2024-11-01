# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import json

import saashq
from saashq import _, throw
from saashq.model.document import Document
from saashq.utils import cint
from saashq.utils.jinja import validate_template


class TermsandConditions(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		buying: DF.Check
		disabled: DF.Check
		selling: DF.Check
		terms: DF.TextEditor | None
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		if self.terms:
			validate_template(self.terms)
		if not cint(self.buying) and not cint(self.selling) and not cint(self.hr) and not cint(self.disabled):
			throw(_("At least one of the Applicable Modules should be selected"))


@saashq.whitelist()
def get_terms_and_conditions(template_name, doc):
	if isinstance(doc, str):
		doc = json.loads(doc)

	terms_and_conditions = saashq.get_doc("Terms and Conditions", template_name)

	if terms_and_conditions.terms:
		return saashq.render_template(terms_and_conditions.terms, doc)
