# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq
from saashq import _, msgprint, scrub, unscrub
from saashq.model.document import Document
from saashq.utils import get_link_to_form, now


class POSProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.accounts.doctype.pos_customer_group.pos_customer_group import POSCustomerGroup
		from erpnexus.accounts.doctype.pos_item_group.pos_item_group import POSItemGroup
		from erpnexus.accounts.doctype.pos_payment_method.pos_payment_method import POSPaymentMethod
		from erpnexus.accounts.doctype.pos_profile_user.pos_profile_user import POSProfileUser

		account_for_change_amount: DF.Link | None
		allow_discount_change: DF.Check
		allow_rate_change: DF.Check
		applicable_for_users: DF.Table[POSProfileUser]
		apply_discount_on: DF.Literal["Grand Total", "Net Total"]
		auto_add_item_to_cart: DF.Check
		company: DF.Link
		company_address: DF.Link | None
		cost_center: DF.Link | None
		country: DF.ReadOnly | None
		currency: DF.Link
		customer: DF.Link | None
		customer_groups: DF.Table[POSCustomerGroup]
		disable_rounded_total: DF.Check
		disabled: DF.Check
		expense_account: DF.Link | None
		hide_images: DF.Check
		hide_unavailable_items: DF.Check
		ignore_pricing_rule: DF.Check
		income_account: DF.Link | None
		item_groups: DF.Table[POSItemGroup]
		letter_head: DF.Link | None
		payments: DF.Table[POSPaymentMethod]
		print_format: DF.Link | None
		select_print_heading: DF.Link | None
		selling_price_list: DF.Link | None
		tax_category: DF.Link | None
		taxes_and_charges: DF.Link | None
		tc_name: DF.Link | None
		update_stock: DF.Check
		utm_campaign: DF.Link | None
		utm_medium: DF.Link | None
		utm_source: DF.Link | None
		validate_stock_on_save: DF.Check
		warehouse: DF.Link
		write_off_account: DF.Link
		write_off_cost_center: DF.Link
		write_off_limit: DF.Currency
	# end: auto-generated types

	def validate(self):
		self.validate_default_profile()
		self.validate_all_link_fields()
		self.validate_duplicate_groups()
		self.validate_payment_methods()
		self.validate_accounting_dimensions()

	def validate_accounting_dimensions(self):
		acc_dim_names = required_accounting_dimensions()
		for acc_dim in acc_dim_names:
			if not self.get(acc_dim):
				saashq.throw(
					_(
						"{0} is a mandatory Accounting Dimension. <br>"
						"Please set a value for {0} in Accounting Dimensions section."
					).format(
						unscrub(saashq.bold(acc_dim)),
					),
					title=_("Mandatory Accounting Dimension"),
				)

	def validate_default_profile(self):
		for row in self.applicable_for_users:
			res = saashq.db.sql(
				"""select pf.name
				from
					`tabPOS Profile User` pfu, `tabPOS Profile` pf
				where
					pf.name = pfu.parent and pfu.user = %s and pf.name != %s and pf.company = %s
					and pfu.default=1 and pf.disabled = 0""",
				(row.user, self.name, self.company),
			)

			if row.default and res:
				msgprint(
					_("Already set default in pos profile {0} for user {1}, kindly disabled default").format(
						res[0][0], row.user
					),
					raise_exception=1,
				)
			elif not row.default and not res:
				msgprint(
					_(
						"User {0} doesn't have any default POS Profile. Check Default at Row {1} for this User."
					).format(row.user, row.idx)
				)

	def validate_all_link_fields(self):
		accounts = {
			"Account": [self.income_account, self.expense_account],
			"Cost Center": [self.cost_center],
			"Warehouse": [self.warehouse],
		}

		for link_dt, dn_list in accounts.items():
			for link_dn in dn_list:
				if link_dn and not saashq.db.exists(
					{"doctype": link_dt, "company": self.company, "name": link_dn}
				):
					saashq.throw(_("{0} does not belong to Company {1}").format(link_dn, self.company))

	def validate_duplicate_groups(self):
		item_groups = [d.item_group for d in self.item_groups]
		customer_groups = [d.customer_group for d in self.customer_groups]

		if len(item_groups) != len(set(item_groups)):
			saashq.throw(
				_("Duplicate item group found in the item group table"), title=_("Duplicate Item Group")
			)

		if len(customer_groups) != len(set(customer_groups)):
			saashq.throw(
				_("Duplicate customer group found in the customer group table"),
				title=_("Duplicate Customer Group"),
			)

	def validate_payment_methods(self):
		if not self.payments:
			saashq.throw(_("Payment methods are mandatory. Please add at least one payment method."))

		default_mode = [d.default for d in self.payments if d.default]
		if not default_mode:
			saashq.throw(_("Please select a default mode of payment"))

		if len(default_mode) > 1:
			saashq.throw(_("You can only select one mode of payment as default"))

		invalid_modes = []
		for d in self.payments:
			account = saashq.db.get_value(
				"Mode of Payment Account",
				{"parent": d.mode_of_payment, "company": self.company},
				"default_account",
			)

			if not account:
				invalid_modes.append(get_link_to_form("Mode of Payment", d.mode_of_payment))

		if invalid_modes:
			if invalid_modes == 1:
				msg = _("Please set default Cash or Bank account in Mode of Payment {}")
			else:
				msg = _("Please set default Cash or Bank account in Mode of Payments {}")
			saashq.throw(msg.format(", ".join(invalid_modes)), title=_("Missing Account"))

	def on_update(self):
		self.set_defaults()

	def on_trash(self):
		self.set_defaults(include_current_pos=False)

	def set_defaults(self, include_current_pos=True):
		saashq.defaults.clear_default("is_pos")

		if not include_current_pos:
			condition = " where pfu.name != '%s' and pfu.default = 1 " % self.name.replace("'", "'")
		else:
			condition = " where pfu.default = 1 "

		pos_view_users = saashq.db.sql_list(
			f"""select pfu.user
			from `tabPOS Profile User` as pfu {condition}"""
		)

		for user in pos_view_users:
			if user:
				saashq.defaults.set_user_default("is_pos", 1, user)
			else:
				saashq.defaults.set_global_default("is_pos", 1)


def get_item_groups(pos_profile):
	item_groups = []
	pos_profile = saashq.get_cached_doc("POS Profile", pos_profile)

	if pos_profile.get("item_groups"):
		# Get items based on the item groups defined in the POS profile
		for data in pos_profile.get("item_groups"):
			item_groups.extend(
				["%s" % saashq.db.escape(d.name) for d in get_child_nodes("Item Group", data.item_group)]
			)

	return list(set(item_groups))


def get_child_nodes(group_type, root):
	lft, rgt = saashq.db.get_value(group_type, root, ["lft", "rgt"])
	return saashq.db.sql(
		f""" Select name, lft, rgt from `tab{group_type}` where
			lft >= {lft} and rgt <= {rgt} order by lft""",
		as_dict=1,
	)


def required_accounting_dimensions():
	p = saashq.qb.DocType("Accounting Dimension")
	c = saashq.qb.DocType("Accounting Dimension Detail")

	acc_dim_doc = (
		saashq.qb.from_(p)
		.inner_join(c)
		.on(p.name == c.parent)
		.select(c.parent)
		.where((c.mandatory_for_bs == 1) | (c.mandatory_for_pl == 1))
		.where(p.disabled == 0)
	).run(as_dict=1)

	acc_dim_names = [scrub(d.parent) for d in acc_dim_doc]
	return acc_dim_names


@saashq.whitelist()
@saashq.validate_and_sanitize_search_inputs
def pos_profile_query(doctype, txt, searchfield, start, page_len, filters):
	user = saashq.session["user"]
	company = filters.get("company") or saashq.defaults.get_user_default("company")

	args = {
		"user": user,
		"start": start,
		"company": company,
		"page_len": page_len,
		"txt": "%%%s%%" % txt,
	}

	pos_profile = saashq.db.sql(
		"""select pf.name
		from
			`tabPOS Profile` pf, `tabPOS Profile User` pfu
		where
			pfu.parent = pf.name and pfu.user = %(user)s and pf.company = %(company)s
			and (pf.name like %(txt)s)
			and pf.disabled = 0 limit %(page_len)s offset %(start)s""",
		args,
	)

	if not pos_profile:
		del args["user"]

		pos_profile = saashq.db.sql(
			"""select pf.name
			from
				`tabPOS Profile` pf left join `tabPOS Profile User` pfu
			on
				pf.name = pfu.parent
			where
				ifnull(pfu.user, '') = ''
				and pf.company = %(company)s
				and pf.name like %(txt)s
				and pf.disabled = 0""",
			args,
		)

	return pos_profile


@saashq.whitelist()
def set_default_profile(pos_profile, company):
	modified = now()
	user = saashq.session.user

	if pos_profile and company:
		saashq.db.sql(
			""" update `tabPOS Profile User` pfu, `tabPOS Profile` pf
			set
				pfu.default = 0, pf.modified = %s, pf.modified_by = %s
			where
				pfu.user = %s and pf.name = pfu.parent and pf.company = %s
				and pfu.default = 1""",
			(modified, user, user, company),
			auto_commit=1,
		)

		saashq.db.sql(
			""" update `tabPOS Profile User` pfu, `tabPOS Profile` pf
			set
				pfu.default = 1, pf.modified = %s, pf.modified_by = %s
			where
				pfu.user = %s and pf.name = pfu.parent and pf.company = %s and pf.name = %s
			""",
			(modified, user, user, company, pos_profile),
			auto_commit=1,
		)
