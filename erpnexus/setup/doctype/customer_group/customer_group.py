# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq
from saashq import _
from saashq.utils.nestedset import NestedSet, get_root_of


class CustomerGroup(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.accounts.doctype.party_account.party_account import PartyAccount
		from erpnexus.selling.doctype.customer_credit_limit.customer_credit_limit import CustomerCreditLimit

		accounts: DF.Table[PartyAccount]
		credit_limits: DF.Table[CustomerCreditLimit]
		customer_group_name: DF.Data
		default_price_list: DF.Link | None
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_customer_group: DF.Link | None
		payment_terms: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	nsm_parent_field = "parent_customer_group"

	def validate(self):
		if not self.parent_customer_group:
			self.parent_customer_group = get_root_of("Customer Group")
		self.validate_currency_for_receivable_and_advance_account()

	def validate_currency_for_receivable_and_advance_account(self):
		for x in self.accounts:
			receivable_account_currency = None
			advance_account_currency = None

			if x.account:
				receivable_account_currency = saashq.get_cached_value(
					"Account", x.account, "account_currency"
				)

			if x.advance_account:
				advance_account_currency = saashq.get_cached_value(
					"Account", x.advance_account, "account_currency"
				)

			if (
				receivable_account_currency
				and advance_account_currency
				and receivable_account_currency != advance_account_currency
			):
				saashq.throw(
					_(
						"Both Receivable Account: {0} and Advance Account: {1} must be of same currency for company: {2}"
					).format(
						saashq.bold(x.account),
						saashq.bold(x.advance_account),
						saashq.bold(x.company),
					)
				)

	def on_update(self):
		super().on_update()
		self.validate_one_root()


def get_parent_customer_groups(customer_group):
	lft, rgt = saashq.db.get_value("Customer Group", customer_group, ["lft", "rgt"])

	return saashq.db.sql(
		"""select name from `tabCustomer Group`
		where lft <= %s and rgt >= %s
		order by lft asc""",
		(lft, rgt),
		as_dict=True,
	)


def on_doctype_update():
	saashq.db.add_index("Customer Group", ["lft", "rgt"])