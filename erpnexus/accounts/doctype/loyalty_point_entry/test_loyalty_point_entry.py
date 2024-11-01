# Copyright (c) 2018, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase
from saashq.utils import today

from erpnexus.accounts.doctype.loyalty_program.test_loyalty_program import create_records
from erpnexus.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice


class TestLoyaltyPointEntry(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		# Create test records
		create_records()
		cls.loyalty_program_name = "Test Single Loyalty"
		cls.customer_name = "Test Loyalty Customer"
		customer = saashq.get_doc("Customer", cls.customer_name)
		customer.db_set("loyalty_program", cls.loyalty_program_name)

	@classmethod
	def tearDownClass(cls):
		# Delete all Loyalty Point Entries
		saashq.db.sql("DELETE FROM `tabLoyalty Point Entry` WHERE customer = %s", cls.customer_name)
		saashq.db.sql("DELETE FROM `tabSales Invoice` WHERE customer = %s", cls.customer_name)
		saashq.db.commit()
		# cls.customer.delete()

	def create_test_invoice(self, redeem=None):
		if redeem:
			si = create_sales_invoice(customer=self.customer_name, qty=1, rate=100, do_not_save=True)
			si.redeem_loyalty_points = True
			si.loyalty_points = redeem
			return si.insert().submit()
		else:
			si = create_sales_invoice(customer=self.customer_name, qty=10, rate=1000, do_not_save=True)
			return si.insert().submit()

	def test_add_loyalty_points(self):
		self.create_test_invoice()
		doc = saashq.get_last_doc("Loyalty Point Entry")
		self.assertEqual(doc.loyalty_points, 10)

	def test_add_loyalty_points_with_discretionary_reason(self):
		doc = saashq.get_doc(
			{
				"doctype": "Loyalty Point Entry",
				"loyalty_program": "Test Single Loyalty",
				"loyalty_program_tier": "Bronce",
				"customer": self.customer_name,
				"invoice_type": "Sales Invoice",
				"loyalty_points": 75,
				"expiry_date": today(),
				"posting_date": today(),
				"company": "_Test Company",
				"discretionary_reason": "Customer Appreciation",
			}
		)
		doc.insert(ignore_permissions=True)
		self.assertEqual(doc.loyalty_points, 75)
		self.assertEqual(doc.discretionary_reason, "Customer Appreciation")

		# Verify the entry in the database
		entry = saashq.get_doc("Loyalty Point Entry", doc.name)
		self.assertEqual(entry.loyalty_points, 75)
		self.assertEqual(entry.discretionary_reason, "Customer Appreciation")

	def test_redeem_loyalty_points(self):
		self.create_test_invoice(redeem=10)
		doc = saashq.get_last_doc("Loyalty Point Entry")
		self.assertEqual(doc.loyalty_points, -10)

		# Check balance
		balance = saashq.db.sql(
			"""
			SELECT SUM(loyalty_points)
			FROM `tabLoyalty Point Entry`
			WHERE customer = %s
		""",
			(self.customer_name,),
		)[0][0]

		self.assertEqual(balance, 75)  # 85 added, 10 redeemed
