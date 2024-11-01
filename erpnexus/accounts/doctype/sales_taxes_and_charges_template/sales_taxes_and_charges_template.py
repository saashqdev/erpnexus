# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq
from saashq import _
from saashq.model.document import Document
from saashq.utils import flt

from erpnexus.controllers.accounts_controller import (
	validate_account_head,
	validate_cost_center,
	validate_inclusive_tax,
	validate_taxes_and_charges,
)


class SalesTaxesandChargesTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.accounts.doctype.sales_taxes_and_charges.sales_taxes_and_charges import (
			SalesTaxesandCharges,
		)

		company: DF.Link
		disabled: DF.Check
		is_default: DF.Check
		tax_category: DF.Link | None
		taxes: DF.Table[SalesTaxesandCharges]
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		valdiate_taxes_and_charges_template(self)

	def autoname(self):
		if self.company and self.title:
			abbr = saashq.get_cached_value("Company", self.company, "abbr")
			self.name = f"{self.title} - {abbr}"

	def set_missing_values(self):
		for data in self.taxes:
			if data.charge_type == "On Net Total" and flt(data.rate) == 0.0:
				data.rate = saashq.get_cached_value("Account", data.account_head, "tax_rate")


def valdiate_taxes_and_charges_template(doc):
	# default should not be disabled
	# if not doc.is_default and not saashq.get_all(doc.doctype, filters={"is_default": 1}):
	# 	doc.is_default = 1

	if doc.is_default == 1:
		saashq.db.sql(
			f"""update `tab{doc.doctype}` set is_default = 0
			where is_default = 1 and name != %s and company = %s""",
			(doc.name, doc.company),
		)

	validate_disabled(doc)

	# Validate with existing taxes and charges template for unique tax category
	validate_for_tax_category(doc)

	for tax in doc.get("taxes"):
		validate_taxes_and_charges(tax)
		validate_account_head(tax.idx, tax.account_head, doc.company, _("Taxes and Charges"))
		validate_cost_center(tax, doc)
		validate_inclusive_tax(tax, doc)


def validate_disabled(doc):
	if doc.is_default and doc.disabled:
		saashq.throw(_("Disabled template must not be default template"))


def validate_for_tax_category(doc):
	if not doc.tax_category:
		return

	if saashq.db.exists(
		doc.doctype,
		{
			"company": doc.company,
			"tax_category": doc.tax_category,
			"disabled": 0,
			"name": ["!=", doc.name],
		},
	):
		saashq.throw(
			_(
				"A template with tax category {0} already exists. Only one template is allowed with each tax category"
			).format(saashq.bold(doc.tax_category))
		)