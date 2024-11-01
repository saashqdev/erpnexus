# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from collections import defaultdict
from itertools import chain

import saashq
from saashq import _
from saashq.query_builder import Interval
from saashq.query_builder.functions import Count, CurDate, UnixTimestamp
from saashq.utils import flt
from saashq.utils.nestedset import NestedSet, get_root_of

from erpnexus import get_default_currency


class SalesPerson(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.setup.doctype.target_detail.target_detail import TargetDetail

		commission_rate: DF.Data | None
		department: DF.Link | None
		employee: DF.Link | None
		enabled: DF.Check
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Data | None
		parent_sales_person: DF.Link | None
		rgt: DF.Int
		sales_person_name: DF.Data
		targets: DF.Table[TargetDetail]
	# end: auto-generated types

	nsm_parent_field = "parent_sales_person"

	def validate(self):
		if not self.parent_sales_person:
			self.parent_sales_person = get_root_of("Sales Person")

		for d in self.get("targets") or []:
			if not flt(d.target_qty) and not flt(d.target_amount):
				saashq.throw(_("Either target qty or target amount is mandatory."))
		self.validate_employee_id()

	def onload(self):
		self.load_dashboard_info()

	def load_dashboard_info(self):
		company_default_currency = get_default_currency()

		allocated_amount_against_order = flt(
			saashq.db.get_value(
				"Sales Team",
				{"docstatus": 1, "parenttype": "Sales Order", "sales_person": self.sales_person_name},
				"sum(allocated_amount)",
			)
		)

		allocated_amount_against_invoice = flt(
			saashq.db.get_value(
				"Sales Team",
				{"docstatus": 1, "parenttype": "Sales Invoice", "sales_person": self.sales_person_name},
				"sum(allocated_amount)",
			)
		)

		info = {}
		info["allocated_amount_against_order"] = allocated_amount_against_order
		info["allocated_amount_against_invoice"] = allocated_amount_against_invoice
		info["currency"] = company_default_currency

		self.set_onload("dashboard_info", info)

	def on_update(self):
		super().on_update()
		self.validate_one_root()

	def get_email_id(self):
		if self.employee:
			user = saashq.db.get_value("Employee", self.employee, "user_id")
			if not user:
				saashq.throw(_("User ID not set for Employee {0}").format(self.employee))
			else:
				return saashq.db.get_value("User", user, "email") or user

	def validate_employee_id(self):
		if self.employee:
			sales_person = saashq.db.get_value("Sales Person", {"employee": self.employee})

			if sales_person and sales_person != self.name:
				saashq.throw(
					_("Another Sales Person {0} exists with the same Employee id").format(sales_person)
				)


def on_doctype_update():
	saashq.db.add_index("Sales Person", ["lft", "rgt"])


def get_timeline_data(doctype: str, name: str) -> dict[int, int]:
	def _fetch_activity(doctype: str, date_field: str):
		sales_team = saashq.qb.DocType("Sales Team")
		transaction = saashq.qb.DocType(doctype)

		return dict(
			saashq.qb.from_(transaction)
			.join(sales_team)
			.on(transaction.name == sales_team.parent)
			.select(UnixTimestamp(transaction[date_field]), Count("*"))
			.where(sales_team.sales_person == name)
			.where(transaction[date_field] > CurDate() - Interval(years=1))
			.groupby(transaction[date_field])
			.run()
		)

	sales_order_activity = _fetch_activity("Sales Order", "transaction_date")
	sales_invoice_activity = _fetch_activity("Sales Invoice", "posting_date")
	delivery_note_activity = _fetch_activity("Delivery Note", "posting_date")

	merged_activities = defaultdict(int)

	for ts, count in chain(
		sales_order_activity.items(), sales_invoice_activity.items(), delivery_note_activity.items()
	):
		merged_activities[ts] += count

	return merged_activities
