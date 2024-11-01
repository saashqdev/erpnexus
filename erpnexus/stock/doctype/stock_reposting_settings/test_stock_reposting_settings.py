# Copyright (c) 2021, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase

from erpnexus.stock.doctype.repost_item_valuation.repost_item_valuation import get_recipients


class TestStockRepostingSettings(IntegrationTestCase):
	def test_notify_reposting_error_to_role(self):
		role = "Notify Reposting Role"

		if not saashq.db.exists("Role", role):
			saashq.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)

		user = "notify_reposting_error@test.com"
		if not saashq.db.exists("User", user):
			saashq.get_doc(
				{
					"doctype": "User",
					"email": user,
					"first_name": "Test",
					"language": "en",
					"time_zone": "Asia/Kolkata",
					"send_welcome_email": 0,
					"roles": [{"role": role}],
				}
			).insert(ignore_permissions=True)

		saashq.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", "")

		users = get_recipients()
		self.assertFalse(user in users)

		saashq.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", role)

		users = get_recipients()
		self.assertTrue(user in users)

	def test_do_reposting_for_each_stock_transaction(self):
		from erpnexus.stock.doctype.item.test_item import make_item
		from erpnexus.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		saashq.db.set_single_value("Stock Reposting Settings", "do_reposting_for_each_stock_transaction", 1)
		if saashq.db.get_single_value("Stock Reposting Settings", "item_based_reposting"):
			saashq.db.set_single_value("Stock Reposting Settings", "item_based_reposting", 0)

		item = make_item(
			"_Test item for reposting check for each transaction", properties={"is_stock_item": 1}
		).name

		stock_entry = make_stock_entry(
			item_code=item,
			qty=1,
			rate=100,
			stock_entry_type="Material Receipt",
			target="_Test Warehouse - _TC",
		)

		riv = saashq.get_all("Repost Item Valuation", filters={"voucher_no": stock_entry.name}, pluck="name")
		self.assertTrue(riv)

		saashq.db.set_single_value("Stock Reposting Settings", "do_reposting_for_each_stock_transaction", 0)

	def test_do_not_reposting_for_each_stock_transaction(self):
		from erpnexus.stock.doctype.item.test_item import make_item
		from erpnexus.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		saashq.db.set_single_value("Stock Reposting Settings", "do_reposting_for_each_stock_transaction", 0)
		if saashq.db.get_single_value("Stock Reposting Settings", "item_based_reposting"):
			saashq.db.set_single_value("Stock Reposting Settings", "item_based_reposting", 0)

		item = make_item(
			"_Test item for do not reposting check for each transaction", properties={"is_stock_item": 1}
		).name

		stock_entry = make_stock_entry(
			item_code=item,
			qty=1,
			rate=100,
			stock_entry_type="Material Receipt",
			target="_Test Warehouse - _TC",
		)

		riv = saashq.get_all("Repost Item Valuation", filters={"voucher_no": stock_entry.name}, pluck="name")
		self.assertFalse(riv)
