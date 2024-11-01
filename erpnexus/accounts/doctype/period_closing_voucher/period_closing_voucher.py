# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import copy

import saashq
from saashq import _
from saashq.query_builder.functions import Sum
from saashq.utils import add_days, flt, formatdate, getdate

from erpnexus.accounts.doctype.account_closing_balance.account_closing_balance import (
	make_closing_entries,
)
from erpnexus.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)
from erpnexus.accounts.utils import get_account_currency, get_fiscal_year
from erpnexus.controllers.accounts_controller import AccountsController


class PeriodClosingVoucher(AccountsController):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		amended_from: DF.Link | None
		closing_account_head: DF.Link
		company: DF.Link
		error_message: DF.Text | None
		fiscal_year: DF.Link
		gle_processing_status: DF.Literal["In Progress", "Completed", "Failed"]
		period_end_date: DF.Date
		period_start_date: DF.Date
		remarks: DF.SmallText
		transaction_date: DF.Date | None
	# end: auto-generated types

	def validate(self):
		self.validate_start_and_end_date()
		self.check_if_previous_year_closed()
		self.block_if_future_closing_voucher_exists()
		self.check_closing_account_type()
		self.check_closing_account_currency()

	def validate_start_and_end_date(self):
		self.fy_start_date, self.fy_end_date = saashq.db.get_value(
			"Fiscal Year", self.fiscal_year, ["year_start_date", "year_end_date"]
		)

		prev_closed_period_end_date = get_previous_closed_period_in_current_year(
			self.fiscal_year, self.company
		)
		valid_start_date = (
			add_days(prev_closed_period_end_date, 1) if prev_closed_period_end_date else self.fy_start_date
		)

		if getdate(self.period_start_date) != getdate(valid_start_date):
			saashq.throw(_("Period Start Date must be {0}").format(formatdate(valid_start_date)))

		if getdate(self.period_start_date) > getdate(self.period_end_date):
			saashq.throw(_("Period Start Date cannot be greater than Period End Date"))

		if getdate(self.period_end_date) > getdate(self.fy_end_date):
			saashq.throw(_("Period End Date cannot be greater than Fiscal Year End Date"))

	def check_if_previous_year_closed(self):
		last_year_closing = add_days(self.fy_start_date, -1)
		previous_fiscal_year = get_fiscal_year(last_year_closing, company=self.company, boolean=True)
		if not previous_fiscal_year:
			return

		previous_fiscal_year_start_date = previous_fiscal_year[0][1]
		gle_exists_in_previous_year = saashq.db.exists(
			"GL Entry",
			{
				"posting_date": ("between", [previous_fiscal_year_start_date, last_year_closing]),
				"company": self.company,
				"is_cancelled": 0,
			},
		)
		if not gle_exists_in_previous_year:
			return

		previous_fiscal_year_closed = saashq.db.exists(
			"Period Closing Voucher",
			{
				"period_end_date": ("between", [previous_fiscal_year_start_date, last_year_closing]),
				"docstatus": 1,
				"company": self.company,
			},
		)
		if not previous_fiscal_year_closed:
			saashq.throw(_("Previous Year is not closed, please close it first"))

	def block_if_future_closing_voucher_exists(self):
		future_closing_voucher = self.get_future_closing_voucher()
		if future_closing_voucher and future_closing_voucher[0][0]:
			action = "cancel" if self.docstatus == 2 else "create"
			saashq.throw(
				_(
					"You cannot {0} this document because another Period Closing Entry {1} exists after {2}"
				).format(action, future_closing_voucher[0][0], self.period_end_date)
			)

	def get_future_closing_voucher(self):
		return saashq.db.get_value(
			"Period Closing Voucher",
			{"period_end_date": (">", self.period_end_date), "docstatus": 1, "company": self.company},
			"name",
		)

	def check_closing_account_type(self):
		closing_account_type = saashq.get_cached_value("Account", self.closing_account_head, "root_type")

		if closing_account_type not in ["Liability", "Equity"]:
			saashq.throw(
				_("Closing Account {0} must be of type Liability / Equity").format(self.closing_account_head)
			)

	def check_closing_account_currency(self):
		account_currency = get_account_currency(self.closing_account_head)
		company_currency = saashq.get_cached_value("Company", self.company, "default_currency")
		if account_currency != company_currency:
			saashq.throw(_("Currency of the Closing Account must be {0}").format(company_currency))

	def on_submit(self):
		self.db_set("gle_processing_status", "In Progress")
		self.make_gl_entries()

	def on_cancel(self):
		self.ignore_linked_doctypes = ("GL Entry", "Stock Ledger Entry", "Payment Ledger Entry")
		self.block_if_future_closing_voucher_exists()
		self.db_set("gle_processing_status", "In Progress")
		self.cancel_gl_entries()

	def make_gl_entries(self):
		if self.get_gle_count_in_selected_period() > 5000:
			saashq.enqueue(
				process_gl_and_closing_entries,
				doc=self,
				timeout=1800,
			)
			saashq.msgprint(
				_(
					"The GL Entries and closing balances will be processed in the background, it can take a few minutes."
				),
				alert=True,
			)
		else:
			process_gl_and_closing_entries(self)

	def get_gle_count_in_selected_period(self):
		return saashq.db.count(
			"GL Entry",
			{
				"posting_date": ["between", [self.period_start_date, self.period_end_date]],
				"company": self.company,
				"is_cancelled": 0,
			},
		)

	def get_pcv_gl_entries(self):
		self.pl_accounts_reverse_gle = []
		self.closing_account_gle = []

		pl_account_balances = self.get_account_balances_based_on_dimensions(report_type="Profit and Loss")
		for dimensions, account_balances in pl_account_balances.items():
			for acc, balances in account_balances.items():
				balance_in_company_currency = flt(balances.debit_in_account_currency) - flt(
					balances.credit_in_account_currency
				)
				if balance_in_company_currency and acc != "balances":
					self.pl_accounts_reverse_gle.append(
						self.get_gle_for_pl_account(acc, balances, dimensions)
					)

			# closing liability account
			self.closing_account_gle.append(
				self.get_gle_for_closing_account(account_balances["balances"], dimensions)
			)

		return self.pl_accounts_reverse_gle + self.closing_account_gle

	def get_gle_for_pl_account(self, acc, balances, dimensions):
		balance_in_account_currency = flt(balances.debit_in_account_currency) - flt(
			balances.credit_in_account_currency
		)
		balance_in_company_currency = flt(balances.debit) - flt(balances.credit)
		gl_entry = saashq._dict(
			{
				"company": self.company,
				"posting_date": self.period_end_date,
				"account": acc,
				"account_currency": balances.account_currency,
				"debit_in_account_currency": abs(balance_in_account_currency)
				if balance_in_account_currency < 0
				else 0,
				"debit": abs(balance_in_company_currency) if balance_in_company_currency < 0 else 0,
				"credit_in_account_currency": abs(balance_in_account_currency)
				if balance_in_account_currency > 0
				else 0,
				"credit": abs(balance_in_company_currency) if balance_in_company_currency > 0 else 0,
				"is_period_closing_voucher_entry": 1,
				"voucher_type": "Period Closing Voucher",
				"voucher_no": self.name,
				"fiscal_year": self.fiscal_year,
				"remarks": self.remarks,
				"is_opening": "No",
			}
		)
		self.update_default_dimensions(gl_entry, dimensions)
		return gl_entry

	def get_gle_for_closing_account(self, dimension_balance, dimensions):
		balance_in_account_currency = flt(dimension_balance.balance_in_account_currency)
		balance_in_company_currency = flt(dimension_balance.balance_in_company_currency)
		gl_entry = saashq._dict(
			{
				"company": self.company,
				"posting_date": self.period_end_date,
				"account": self.closing_account_head,
				"account_currency": saashq.db.get_value(
					"Account", self.closing_account_head, "account_currency"
				),
				"debit_in_account_currency": balance_in_account_currency
				if balance_in_account_currency > 0
				else 0,
				"debit": balance_in_company_currency if balance_in_company_currency > 0 else 0,
				"credit_in_account_currency": abs(balance_in_account_currency)
				if balance_in_account_currency < 0
				else 0,
				"credit": abs(balance_in_company_currency) if balance_in_company_currency < 0 else 0,
				"is_period_closing_voucher_entry": 1,
				"voucher_type": "Period Closing Voucher",
				"voucher_no": self.name,
				"fiscal_year": self.fiscal_year,
				"remarks": self.remarks,
				"is_opening": "No",
			}
		)
		self.update_default_dimensions(gl_entry, dimensions)
		return gl_entry

	def update_default_dimensions(self, gl_entry, dimensions):
		for i, dimension in enumerate(self.accounting_dimension_fields):
			gl_entry[dimension] = dimensions[i]

	def get_account_balances_based_on_dimensions(self, report_type):
		"""Get balance for dimension-wise pl accounts"""
		self.get_accounting_dimension_fields()
		acc_bal_dict = saashq._dict()
		gl_entries = []

		with saashq.db.unbuffered_cursor():
			gl_entries = self.get_gl_entries_for_current_period(report_type, as_iterator=True)
			for gle in gl_entries:
				acc_bal_dict = self.set_account_balance_dict(gle, acc_bal_dict)

		if report_type == "Balance Sheet" and self.is_first_period_closing_voucher():
			opening_entries = self.get_gl_entries_for_current_period(report_type, only_opening_entries=True)
			for gle in opening_entries:
				acc_bal_dict = self.set_account_balance_dict(gle, acc_bal_dict)

		return acc_bal_dict

	def get_accounting_dimension_fields(self):
		default_dimensions = ["cost_center", "finance_book", "project"]
		self.accounting_dimension_fields = default_dimensions + get_accounting_dimensions()

	def get_gl_entries_for_current_period(self, report_type, only_opening_entries=False, as_iterator=False):
		date_condition = ""
		if only_opening_entries:
			date_condition = "is_opening = 'Yes'"
		else:
			date_condition = f"posting_date BETWEEN '{self.period_start_date}' AND '{self.period_end_date}' and is_opening = 'No'"

		# nosemgrep
		return saashq.db.sql(
			"""
			SELECT
				name,
				posting_date,
				account,
				account_currency,
				debit_in_account_currency,
				credit_in_account_currency,
				debit,
				credit,
				{}
			FROM `tabGL Entry`
			WHERE
				{}
				AND company = %s
				AND voucher_type != 'Period Closing Voucher'
				AND EXISTS(SELECT name FROM `tabAccount` WHERE name = account AND report_type = %s)
				AND is_cancelled = 0
			""".format(
				", ".join(self.accounting_dimension_fields),
				date_condition,
			),
			(self.company, report_type),
			as_dict=1,
			as_iterator=as_iterator,
		)

	def set_account_balance_dict(self, gle, acc_bal_dict):
		key = self.get_key(gle)

		acc_bal_dict.setdefault(key, saashq._dict()).setdefault(
			gle.account,
			saashq._dict(
				{
					"debit_in_account_currency": 0,
					"credit_in_account_currency": 0,
					"debit": 0,
					"credit": 0,
					"account_currency": gle.account_currency,
				}
			),
		)

		acc_bal_dict[key][gle.account].debit_in_account_currency += flt(gle.debit_in_account_currency)
		acc_bal_dict[key][gle.account].credit_in_account_currency += flt(gle.credit_in_account_currency)
		acc_bal_dict[key][gle.account].debit += flt(gle.debit)
		acc_bal_dict[key][gle.account].credit += flt(gle.credit)

		# dimension-wise total balances
		acc_bal_dict[key].setdefault(
			"balances",
			saashq._dict(
				{
					"balance_in_account_currency": 0,
					"balance_in_company_currency": 0,
				}
			),
		)

		balance_in_account_currency = flt(gle.debit_in_account_currency) - flt(gle.credit_in_account_currency)
		balance_in_company_currency = flt(gle.debit) - flt(gle.credit)

		acc_bal_dict[key]["balances"].balance_in_account_currency += balance_in_account_currency
		acc_bal_dict[key]["balances"].balance_in_company_currency += balance_in_company_currency

		return acc_bal_dict

	def get_key(self, gle):
		return tuple([gle.get(dimension) for dimension in self.accounting_dimension_fields])

	def get_account_closing_balances(self):
		pl_closing_entries = self.get_closing_entries_for_pl_accounts()
		bs_closing_entries = self.get_closing_entries_for_balance_sheet_accounts()
		closing_entries_for_closing_account = self.get_closing_entries_for_closing_account()
		closing_entries = pl_closing_entries + bs_closing_entries + closing_entries_for_closing_account
		return closing_entries

	def get_closing_entries_for_pl_accounts(self):
		closing_entries = copy.deepcopy(self.pl_accounts_reverse_gle)
		for d in self.pl_accounts_reverse_gle:
			# reverse debit and credit
			gle_copy = copy.deepcopy(d)
			gle_copy.debit = d.credit
			gle_copy.credit = d.debit
			gle_copy.debit_in_account_currency = d.credit_in_account_currency
			gle_copy.credit_in_account_currency = d.debit_in_account_currency
			gle_copy.is_period_closing_voucher_entry = 0
			gle_copy.period_closing_voucher = self.name
			closing_entries.append(gle_copy)

		return closing_entries

	def get_closing_entries_for_balance_sheet_accounts(self):
		closing_entries = []
		balance_sheet_account_balances = self.get_account_balances_based_on_dimensions(
			report_type="Balance Sheet"
		)

		for dimensions, account_balances in balance_sheet_account_balances.items():
			for acc, balances in account_balances.items():
				balance_in_company_currency = flt(balances.debit) - flt(balances.credit)
				if acc != "balances" and balance_in_company_currency:
					closing_entries.append(self.get_closing_entry(acc, balances, dimensions))

		return closing_entries

	def get_closing_entry(self, account, balances, dimensions):
		closing_entry = saashq._dict(
			{
				"company": self.company,
				"closing_date": self.period_end_date,
				"period_closing_voucher": self.name,
				"account": account,
				"account_currency": balances.account_currency,
				"debit_in_account_currency": flt(balances.debit_in_account_currency),
				"debit": flt(balances.debit),
				"credit_in_account_currency": flt(balances.credit_in_account_currency),
				"credit": flt(balances.credit),
				"is_period_closing_voucher_entry": 0,
			}
		)
		self.update_default_dimensions(closing_entry, dimensions)
		return closing_entry

	def get_closing_entries_for_closing_account(self):
		closing_entries = copy.deepcopy(self.closing_account_gle)
		for d in closing_entries:
			d.period_closing_voucher = self.name

		return closing_entries

	def is_first_period_closing_voucher(self):
		first_pcv = saashq.db.get_value(
			"Period Closing Voucher",
			{"company": self.company, "docstatus": 1},
			"name",
			order_by="period_end_date",
		)

		if not first_pcv or first_pcv == self.name:
			return True

	def cancel_gl_entries(self):
		if self.get_gle_count_against_current_pcv() > 5000:
			saashq.enqueue(
				process_cancellation,
				voucher_type="Period Closing Voucher",
				voucher_no=self.name,
				queue="long",
				enqueue_after_commit=True,
			)
			saashq.msgprint(
				_("The GL Entries will be cancelled in the background, it can take a few minutes."),
				alert=True,
			)
		else:
			process_cancellation(voucher_type="Period Closing Voucher", voucher_no=self.name)

	def get_gle_count_against_current_pcv(self):
		return saashq.db.count(
			"GL Entry",
			{"voucher_type": "Period Closing Voucher", "voucher_no": self.name, "is_cancelled": 0},
		)


def process_gl_and_closing_entries(doc):
	from erpnexus.accounts.general_ledger import make_gl_entries

	try:
		gl_entries = doc.get_pcv_gl_entries()
		if gl_entries:
			make_gl_entries(gl_entries, merge_entries=False)

		closing_entries = doc.get_account_closing_balances()
		make_closing_entries(closing_entries, doc.name, doc.company, doc.period_end_date)

		saashq.db.set_value(doc.doctype, doc.name, "gle_processing_status", "Completed")
	except Exception as e:
		saashq.db.rollback()
		saashq.log_error(e)
		saashq.db.set_value(doc.doctype, doc.name, "gle_processing_status", "Failed")


def process_cancellation(voucher_type, voucher_no):
	from erpnexus.accounts.general_ledger import make_reverse_gl_entries

	try:
		make_reverse_gl_entries(voucher_type=voucher_type, voucher_no=voucher_no)
		delete_closing_entries(voucher_no)
		saashq.db.set_value("Period Closing Voucher", voucher_no, "gle_processing_status", "Completed")
	except Exception as e:
		saashq.db.rollback()
		saashq.log_error(e)
		saashq.db.set_value("Period Closing Voucher", voucher_no, "gle_processing_status", "Failed")


def delete_closing_entries(voucher_no):
	closing_balance = saashq.qb.DocType("Account Closing Balance")
	saashq.qb.from_(closing_balance).delete().where(
		closing_balance.period_closing_voucher == voucher_no
	).run()


@saashq.whitelist()
def get_period_start_end_date(fiscal_year, company):
	fy_start_date, fy_end_date = saashq.db.get_value(
		"Fiscal Year", fiscal_year, ["year_start_date", "year_end_date"]
	)
	prev_closed_period_end_date = get_previous_closed_period_in_current_year(fiscal_year, company)
	period_start_date = (
		add_days(prev_closed_period_end_date, 1) if prev_closed_period_end_date else fy_start_date
	)
	return period_start_date, fy_end_date


def get_previous_closed_period_in_current_year(fiscal_year, company):
	prev_closed_period_end_date = saashq.db.get_value(
		"Period Closing Voucher",
		filters={
			"company": company,
			"fiscal_year": fiscal_year,
			"docstatus": 1,
		},
		fieldname=["period_end_date"],
		order_by="period_end_date desc",
	)
	return prev_closed_period_end_date
