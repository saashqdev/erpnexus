# Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import saashq
from saashq import _
from saashq.model.document import Document
from saashq.utils import add_to_date, get_datetime, get_time_str, time_diff_in_hours


class StockRepostingSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		do_reposting_for_each_stock_transaction: DF.Check
		end_time: DF.Time | None
		item_based_reposting: DF.Check
		limit_reposting_timeslot: DF.Check
		limits_dont_apply_on: DF.Literal[
			"", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
		]
		notify_reposting_error_to_role: DF.Link | None
		start_time: DF.Time | None
	# end: auto-generated types

	def validate(self):
		self.set_minimum_reposting_time_slot()

	def before_save(self):
		if self.do_reposting_for_each_stock_transaction:
			self.item_based_reposting = 1

	def set_minimum_reposting_time_slot(self):
		"""Ensure that timeslot for reposting is at least 12 hours."""
		if not self.limit_reposting_timeslot:
			return

		start_time = get_datetime(self.start_time)
		end_time = get_datetime(self.end_time)

		if start_time > end_time:
			end_time = add_to_date(end_time, days=1, as_datetime=True)

		diff = time_diff_in_hours(end_time, start_time)

		if diff < 10:
			self.end_time = get_time_str(add_to_date(self.start_time, hours=10, as_datetime=True))

	@saashq.whitelist()
	def convert_to_item_wh_reposting(self):
		"""Convert Transaction reposting to Item Warehouse based reposting if Item Based Reposting has enabled."""

		reposting_data = get_reposting_entries()

		vouchers = [d.voucher_no for d in reposting_data]

		item_warehouses = {}

		for ledger in get_stock_ledgers(vouchers):
			key = (ledger.item_code, ledger.warehouse)
			if key not in item_warehouses:
				item_warehouses[key] = ledger.posting_date
			elif saashq.utils.getdate(item_warehouses.get(key)) > saashq.utils.getdate(ledger.posting_date):
				item_warehouses[key] = ledger.posting_date

		for key, posting_date in item_warehouses.items():
			item_code, warehouse = key
			create_repost_item_valuation(item_code, warehouse, posting_date)

		for row in reposting_data:
			saashq.db.set_value("Repost Item Valuation", row.name, "status", "Skipped")

		self.db_set("item_based_reposting", 1)
		saashq.msgprint(_("Item Warehouse based reposting has been enabled."))


def get_reposting_entries():
	return saashq.get_all(
		"Repost Item Valuation",
		fields=["voucher_no", "name"],
		filters={"status": ("in", ["Queued", "In Progress"]), "docstatus": 1, "based_on": "Transaction"},
	)


def get_stock_ledgers(vouchers):
	return saashq.get_all(
		"Stock Ledger Entry",
		fields=["item_code", "warehouse", "posting_date"],
		filters={"voucher_no": ("in", vouchers)},
	)


def create_repost_item_valuation(item_code, warehouse, posting_date):
	saashq.get_doc(
		{
			"doctype": "Repost Item Valuation",
			"company": saashq.get_cached_value("Warehouse", warehouse, "company"),
			"posting_date": posting_date,
			"based_on": "Item and Warehouse",
			"posting_time": "00:00:01",
			"item_code": item_code,
			"warehouse": warehouse,
			"allow_negative_stock": True,
			"status": "Queued",
		}
	).submit()
