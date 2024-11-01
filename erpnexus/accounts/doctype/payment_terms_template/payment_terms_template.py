# Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.model.document import Document
from saashq.utils import flt


class PaymentTermsTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.accounts.doctype.payment_terms_template_detail.payment_terms_template_detail import (
			PaymentTermsTemplateDetail,
		)

		allocate_payment_based_on_payment_terms: DF.Check
		template_name: DF.Data | None
		terms: DF.Table[PaymentTermsTemplateDetail]
	# end: auto-generated types

	def validate(self):
		self.validate_invoice_portion()
		self.validate_terms()

	def validate_invoice_portion(self):
		total_portion = 0
		for term in self.terms:
			total_portion += flt(term.get("invoice_portion", 0))

		if flt(total_portion, 2) != 100.00:
			saashq.msgprint(_("Combined invoice portion must equal 100%"), raise_exception=1, indicator="red")

	def validate_terms(self):
		terms = []
		for term in self.terms:
			if self.allocate_payment_based_on_payment_terms and not term.payment_term:
				saashq.throw(_("Row {0}: Payment Term is mandatory").format(term.idx))

			term_info = (term.payment_term, term.credit_days, term.credit_months, term.due_date_based_on)
			if term_info in terms:
				saashq.msgprint(
					_("The Payment Term at row {0} is possibly a duplicate.").format(term.idx),
					raise_exception=1,
					indicator="red",
				)
			else:
				terms.append(term_info)
