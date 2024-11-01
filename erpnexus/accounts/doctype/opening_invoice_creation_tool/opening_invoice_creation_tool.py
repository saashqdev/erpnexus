# Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _, scrub
from saashq.model.document import Document
from saashq.utils import flt, nowdate
from saashq.utils.background_jobs import enqueue, is_job_enqueued

from erpnexus.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)


class OpeningInvoiceCreationTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.accounts.doctype.opening_invoice_creation_tool_item.opening_invoice_creation_tool_item import (
			OpeningInvoiceCreationToolItem,
		)

		company: DF.Link
		cost_center: DF.Link | None
		create_missing_party: DF.Check
		invoice_type: DF.Literal["Sales", "Purchase"]
		invoices: DF.Table[OpeningInvoiceCreationToolItem]
	# end: auto-generated types

	def onload(self):
		"""Load the Opening Invoice summary"""
		summary, max_count = self.get_opening_invoice_summary()
		self.set_onload("opening_invoices_summary", summary)
		self.set_onload("max_count", max_count)
		self.set_onload("temporary_opening_account", get_temporary_opening_account(self.company))

	def get_opening_invoice_summary(self):
		def prepare_invoice_summary(doctype, invoices):
			# add company wise sales / purchase invoice summary
			paid_amount = []
			outstanding_amount = []
			for invoice in invoices:
				company = invoice.pop("company")
				_summary = invoices_summary.get(company, {})
				_summary.update({"currency": company_wise_currency.get(company), doctype: invoice})
				invoices_summary.update({company: _summary})

				if invoice.paid_amount:
					paid_amount.append(invoice.paid_amount)
				if invoice.outstanding_amount:
					outstanding_amount.append(invoice.outstanding_amount)

			if paid_amount or outstanding_amount:
				max_count.update(
					{
						doctype: {
							"max_paid": max(paid_amount) if paid_amount else 0.0,
							"max_due": max(outstanding_amount) if outstanding_amount else 0.0,
						}
					}
				)

		invoices_summary = {}
		max_count = {}
		fields = [
			"company",
			"count(name) as total_invoices",
			"sum(outstanding_amount) as outstanding_amount",
		]
		companies = saashq.get_all("Company", fields=["name as company", "default_currency as currency"])
		if not companies:
			return None, None

		company_wise_currency = {row.company: row.currency for row in companies}
		for doctype in ["Sales Invoice", "Purchase Invoice"]:
			invoices = saashq.get_all(
				doctype, filters=dict(is_opening="Yes", docstatus=1), fields=fields, group_by="company"
			)
			prepare_invoice_summary(doctype, invoices)

		return invoices_summary, max_count

	def validate_company(self):
		if not self.company:
			saashq.throw(_("Please select the Company"))

	def set_missing_values(self, row):
		row.qty = row.qty or 1.0
		row.temporary_opening_account = row.temporary_opening_account or get_temporary_opening_account(
			self.company
		)
		row.party_type = "Customer" if self.invoice_type == "Sales" else "Supplier"
		row.item_name = row.item_name or _("Opening Invoice Item")
		row.posting_date = row.posting_date or nowdate()
		row.due_date = row.due_date or nowdate()

	def validate_mandatory_invoice_fields(self, row):
		if not saashq.db.exists(row.party_type, row.party):
			if self.create_missing_party:
				self.add_party(row.party_type, row.party)
			else:
				saashq.throw(
					_("Row #{}: {} {} does not exist.").format(
						row.idx, saashq.bold(row.party_type), saashq.bold(row.party)
					)
				)

		mandatory_error_msg = _("Row #{0}: {1} is required to create the Opening {2} Invoices")
		for d in ("Party", "Outstanding Amount", "Temporary Opening Account"):
			if not row.get(scrub(d)):
				saashq.throw(mandatory_error_msg.format(row.idx, d, self.invoice_type))

	def get_invoices(self):
		invoices = []
		for row in self.invoices:
			if not row:
				continue
			self.set_missing_values(row)
			self.validate_mandatory_invoice_fields(row)
			invoice = self.get_invoice_dict(row)
			company_details = (
				saashq.get_cached_value(
					"Company", self.company, ["default_currency", "default_letter_head"], as_dict=1
				)
				or {}
			)

			default_currency = saashq.db.get_value(row.party_type, row.party, "default_currency")

			if company_details:
				invoice.update(
					{
						"currency": default_currency or company_details.get("default_currency"),
						"letter_head": company_details.get("default_letter_head"),
					}
				)
			invoices.append(invoice)

		return invoices

	def add_party(self, party_type, party):
		party_doc = saashq.new_doc(party_type)
		if party_type == "Customer":
			party_doc.customer_name = party
		else:
			supplier_group = saashq.db.get_single_value("Buying Settings", "supplier_group")
			if not supplier_group:
				saashq.throw(_("Please Set Supplier Group in Buying Settings."))

			party_doc.supplier_name = party
			party_doc.supplier_group = supplier_group

		party_doc.flags.ignore_mandatory = True
		party_doc.save(ignore_permissions=True)

	def get_invoice_dict(self, row=None):
		def get_item_dict():
			cost_center = row.get("cost_center") or saashq.get_cached_value(
				"Company", self.company, "cost_center"
			)
			if not cost_center:
				saashq.throw(
					_("Please set the Default Cost Center in {0} company.").format(saashq.bold(self.company))
				)

			income_expense_account_field = (
				"income_account" if row.party_type == "Customer" else "expense_account"
			)
			default_uom = saashq.db.get_single_value("Stock Settings", "stock_uom") or "Nos"
			rate = flt(row.outstanding_amount) / flt(row.qty)

			item_dict = saashq._dict(
				{
					"uom": default_uom,
					"rate": rate or 0.0,
					"qty": row.qty,
					"conversion_factor": 1.0,
					"item_name": row.item_name or "Opening Invoice Item",
					"description": row.item_name or "Opening Invoice Item",
					income_expense_account_field: row.temporary_opening_account,
					"cost_center": cost_center,
				}
			)

			for dimension in get_accounting_dimensions():
				item_dict.update({dimension: row.get(dimension)})

			return item_dict

		item = get_item_dict()

		invoice = saashq._dict(
			{
				"items": [item],
				"is_opening": "Yes",
				"set_posting_time": 1,
				"company": self.company,
				"cost_center": self.cost_center,
				"due_date": row.due_date,
				"posting_date": row.posting_date,
				saashq.scrub(row.party_type): row.party,
				"is_pos": 0,
				"doctype": "Sales Invoice" if self.invoice_type == "Sales" else "Purchase Invoice",
				"update_stock": 0,  # important: https://github.com/saashqdev/erpnexus/pull/23559
				"invoice_number": row.invoice_number,
				"disable_rounded_total": 1,
			}
		)

		accounting_dimension = get_accounting_dimensions()
		for dimension in accounting_dimension:
			invoice.update({dimension: self.get(dimension) or item.get(dimension)})

		return invoice

	@saashq.whitelist()
	def make_invoices(self):
		self.validate_company()
		invoices = self.get_invoices()
		if len(invoices) < 50:
			return start_import(invoices)
		else:
			from saashq.utils.scheduler import is_scheduler_inactive

			if is_scheduler_inactive() and not saashq.flags.in_test:
				saashq.throw(_("Scheduler is inactive. Cannot import data."), title=_("Scheduler Inactive"))

			job_id = f"opening_invoice::{self.name}"

			if not is_job_enqueued(job_id):
				enqueue(
					start_import,
					queue="default",
					timeout=6000,
					event="opening_invoice_creation",
					job_id=job_id,
					invoices=invoices,
					now=saashq.conf.developer_mode or saashq.flags.in_test,
				)


def start_import(invoices):
	errors = 0
	names = []
	for idx, d in enumerate(invoices):
		try:
			invoice_number = None
			if d.invoice_number:
				invoice_number = d.invoice_number
			publish(idx, len(invoices), d.doctype)
			doc = saashq.get_doc(d)
			doc.flags.ignore_mandatory = True
			doc.insert(set_name=invoice_number)
			doc.submit()
			saashq.db.commit()
			names.append(doc.name)
		except Exception:
			errors += 1
			saashq.db.rollback()
			doc.log_error("Opening invoice creation failed")
	if errors:
		saashq.msgprint(
			_("You had {} errors while creating opening invoices. Check {} for more details").format(
				errors, "<a href='/app/List/Error Log' class='variant-click'>Error Log</a>"
			),
			indicator="red",
			title=_("Error Occurred"),
		)
	return names


def publish(index, total, doctype):
	saashq.publish_realtime(
		"opening_invoice_creation_progress",
		dict(
			title=_("Opening Invoice Creation In Progress"),
			message=_("Creating {} out of {} {}").format(index + 1, total, doctype),
			count=index + 1,
			total=total,
		),
		user=saashq.session.user,
	)


@saashq.whitelist()
def get_temporary_opening_account(company=None):
	if not company:
		return

	accounts = saashq.get_all("Account", filters={"company": company, "account_type": "Temporary"})
	if not accounts:
		saashq.throw(_("Please add a Temporary Opening account in Chart of Accounts"))

	return accounts[0].name
