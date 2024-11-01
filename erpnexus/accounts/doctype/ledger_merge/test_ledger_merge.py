# Copyright (c) 2021, Wahni Green Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase

from erpnexus.accounts.doctype.ledger_merge.ledger_merge import start_merge


class TestLedgerMerge(IntegrationTestCase):
	def test_merge_success(self):
		if not saashq.db.exists("Account", "Indirect Expenses - _TC"):
			acc = saashq.new_doc("Account")
			acc.account_name = "Indirect Expenses"
			acc.is_group = 1
			acc.parent_account = "Expenses - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not saashq.db.exists("Account", "Indirect Test Expenses - _TC"):
			acc = saashq.new_doc("Account")
			acc.account_name = "Indirect Test Expenses"
			acc.is_group = 1
			acc.parent_account = "Expenses - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not saashq.db.exists("Account", "Administrative Test Expenses - _TC"):
			acc = saashq.new_doc("Account")
			acc.account_name = "Administrative Test Expenses"
			acc.parent_account = "Indirect Test Expenses - _TC"
			acc.company = "_Test Company"
			acc.insert()

		doc = saashq.get_doc(
			{
				"doctype": "Ledger Merge",
				"company": "_Test Company",
				"root_type": saashq.db.get_value("Account", "Indirect Test Expenses - _TC", "root_type"),
				"account": "Indirect Expenses - _TC",
				"merge_accounts": [
					{"account": "Indirect Test Expenses - _TC", "account_name": "Indirect Expenses"}
				],
			}
		).insert(ignore_permissions=True)

		parent = saashq.db.get_value("Account", "Administrative Test Expenses - _TC", "parent_account")
		self.assertEqual(parent, "Indirect Test Expenses - _TC")

		start_merge(doc.name)

		parent = saashq.db.get_value("Account", "Administrative Test Expenses - _TC", "parent_account")
		self.assertEqual(parent, "Indirect Expenses - _TC")

		self.assertFalse(saashq.db.exists("Account", "Indirect Test Expenses - _TC"))

	def test_partial_merge_success(self):
		if not saashq.db.exists("Account", "Indirect Income - _TC"):
			acc = saashq.new_doc("Account")
			acc.account_name = "Indirect Income"
			acc.is_group = 1
			acc.parent_account = "Income - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not saashq.db.exists("Account", "Indirect Test Income - _TC"):
			acc = saashq.new_doc("Account")
			acc.account_name = "Indirect Test Income"
			acc.is_group = 1
			acc.parent_account = "Income - _TC"
			acc.company = "_Test Company"
			acc.insert()
		if not saashq.db.exists("Account", "Administrative Test Income - _TC"):
			acc = saashq.new_doc("Account")
			acc.account_name = "Administrative Test Income"
			acc.parent_account = "Indirect Test Income - _TC"
			acc.company = "_Test Company"
			acc.insert()

		doc = saashq.get_doc(
			{
				"doctype": "Ledger Merge",
				"company": "_Test Company",
				"root_type": saashq.db.get_value("Account", "Indirect Income - _TC", "root_type"),
				"account": "Indirect Income - _TC",
				"merge_accounts": [
					{"account": "Indirect Test Income - _TC", "account_name": "Indirect Test Income"},
					{
						"account": "Administrative Test Income - _TC",
						"account_name": "Administrative Test Income",
					},
				],
			}
		).insert(ignore_permissions=True)

		parent = saashq.db.get_value("Account", "Administrative Test Income - _TC", "parent_account")
		self.assertEqual(parent, "Indirect Test Income - _TC")

		start_merge(doc.name)

		parent = saashq.db.get_value("Account", "Administrative Test Income - _TC", "parent_account")
		self.assertEqual(parent, "Indirect Income - _TC")

		self.assertFalse(saashq.db.exists("Account", "Indirect Test Income - _TC"))
		self.assertTrue(saashq.db.exists("Account", "Administrative Test Income - _TC"))

	def tearDown(self):
		for entry in saashq.db.get_all("Ledger Merge"):
			saashq.delete_doc("Ledger Merge", entry.name)

		test_accounts = [
			"Indirect Test Expenses - _TC",
			"Administrative Test Expenses - _TC",
			"Indirect Test Income - _TC",
			"Administrative Test Income - _TC",
		]
		for account in test_accounts:
			saashq.delete_doc_if_exists("Account", account)
