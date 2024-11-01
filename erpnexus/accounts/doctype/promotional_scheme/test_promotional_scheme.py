# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase

from erpnexus.accounts.doctype.promotional_scheme.promotional_scheme import TransactionExists
from erpnexus.selling.doctype.sales_order.test_sales_order import make_sales_order


class TestPromotionalScheme(IntegrationTestCase):
	def setUp(self):
		if saashq.db.exists("Promotional Scheme", "_Test Scheme"):
			saashq.delete_doc("Promotional Scheme", "_Test Scheme")

	def test_promotional_scheme(self):
		ps = make_promotional_scheme(applicable_for="Customer", customer="_Test Customer")
		price_rules = saashq.get_all(
			"Pricing Rule",
			fields=["promotional_scheme_id", "name", "creation"],
			filters={"promotional_scheme": ps.name},
		)
		self.assertTrue(len(price_rules), 1)
		price_doc_details = saashq.db.get_value(
			"Pricing Rule", price_rules[0].name, ["customer", "min_qty", "discount_percentage"], as_dict=1
		)
		self.assertTrue(price_doc_details.customer, "_Test Customer")
		self.assertTrue(price_doc_details.min_qty, 4)
		self.assertTrue(price_doc_details.discount_percentage, 20)

		ps.price_discount_slabs[0].min_qty = 6
		ps.append("customer", {"customer": "_Test Customer 2"})
		ps.save()
		price_rules = saashq.get_all(
			"Pricing Rule",
			fields=["promotional_scheme_id", "name"],
			filters={"promotional_scheme": ps.name},
		)
		self.assertTrue(len(price_rules), 2)

		price_doc_details = saashq.db.get_value(
			"Pricing Rule", price_rules[1].name, ["customer", "min_qty", "discount_percentage"], as_dict=1
		)
		self.assertTrue(price_doc_details.customer, "_Test Customer 2")
		self.assertTrue(price_doc_details.min_qty, 6)
		self.assertTrue(price_doc_details.discount_percentage, 20)

		price_doc_details = saashq.db.get_value(
			"Pricing Rule", price_rules[0].name, ["customer", "min_qty", "discount_percentage"], as_dict=1
		)
		self.assertTrue(price_doc_details.customer, "_Test Customer")
		self.assertTrue(price_doc_details.min_qty, 6)

		saashq.delete_doc("Promotional Scheme", ps.name)
		price_rules = saashq.get_all(
			"Pricing Rule",
			fields=["promotional_scheme_id", "name"],
			filters={"promotional_scheme": ps.name},
		)
		self.assertEqual(price_rules, [])

	def test_promotional_scheme_without_applicable_for(self):
		ps = make_promotional_scheme()
		price_rules = saashq.get_all("Pricing Rule", filters={"promotional_scheme": ps.name})

		self.assertTrue(len(price_rules), 1)
		saashq.delete_doc("Promotional Scheme", ps.name)

		price_rules = saashq.get_all("Pricing Rule", filters={"promotional_scheme": ps.name})
		self.assertEqual(price_rules, [])

	def test_change_applicable_for_in_promotional_scheme(self):
		ps = make_promotional_scheme()
		price_rules = saashq.get_all("Pricing Rule", filters={"promotional_scheme": ps.name})
		self.assertTrue(len(price_rules), 1)

		so = make_sales_order(qty=5, currency="USD", do_not_save=True)
		so.set_missing_values()
		so.save()
		self.assertEqual(price_rules[0].name, so.pricing_rules[0].pricing_rule)

		ps.applicable_for = "Customer"
		ps.append("customer", {"customer": "_Test Customer"})

		self.assertRaises(TransactionExists, ps.save)

		saashq.delete_doc("Sales Order", so.name)
		saashq.delete_doc("Promotional Scheme", ps.name)
		price_rules = saashq.get_all("Pricing Rule", filters={"promotional_scheme": ps.name})
		self.assertEqual(price_rules, [])

	def test_change_applicable_for_values_in_promotional_scheme(self):
		ps = make_promotional_scheme(applicable_for="Customer", customer="_Test Customer")
		ps.append("customer", {"customer": "_Test Customer 2"})
		ps.save()

		price_rules = saashq.get_all(
			"Pricing Rule", filters={"promotional_scheme": ps.name, "applicable_for": "Customer"}
		)
		self.assertTrue(len(price_rules), 2)

		ps.set("customer", [])
		ps.append("customer", {"customer": "_Test Customer 2"})
		ps.save()

		price_rules = saashq.get_all(
			"Pricing Rule",
			filters={
				"promotional_scheme": ps.name,
				"applicable_for": "Customer",
				"customer": "_Test Customer",
			},
		)
		self.assertEqual(price_rules, [])
		saashq.delete_doc("Promotional Scheme", ps.name)

	def test_min_max_amount_configuration(self):
		ps = make_promotional_scheme()
		ps.price_discount_slabs[0].min_amount = 10
		ps.price_discount_slabs[0].max_amount = 1000
		ps.save()

		price_rules_data = saashq.db.get_value(
			"Pricing Rule", {"promotional_scheme": ps.name}, ["min_amt", "max_amt"], as_dict=1
		)

		self.assertEqual(price_rules_data.min_amt, 10)
		self.assertEqual(price_rules_data.max_amt, 1000)

		saashq.delete_doc("Promotional Scheme", ps.name)
		price_rules = saashq.get_all("Pricing Rule", filters={"promotional_scheme": ps.name})
		self.assertEqual(price_rules, [])

	def test_pricing_rule_for_product_discount_slabs(self):
		ps = make_promotional_scheme()
		ps.set("price_discount_slabs", [])
		ps.set(
			"product_discount_slabs",
			[
				{
					"rule_description": "12+1",
					"min_qty": 12,
					"free_item": "_Test Item 2",
					"free_qty": 1,
					"is_recursive": 1,
					"recurse_for": 12,
				}
			],
		)
		ps.save()
		pr = saashq.get_doc("Pricing Rule", {"promotional_scheme_id": ps.product_discount_slabs[0].name})
		self.assertSequenceEqual(
			[pr.min_qty, pr.free_item, pr.free_qty, pr.recurse_for], [12, "_Test Item 2", 1, 12]
		)

	def test_validation_on_recurse_with_mixed_condition(self):
		ps = make_promotional_scheme()
		ps.set("price_discount_slabs", [])
		ps.set(
			"product_discount_slabs",
			[
				{
					"rule_description": "12+1",
					"min_qty": 12,
					"free_item": "_Test Item 2",
					"free_qty": 1,
					"is_recursive": 1,
					"recurse_for": 12,
				}
			],
		)
		ps.mixed_conditions = True
		self.assertRaises(saashq.ValidationError, ps.save)


def make_promotional_scheme(**args):
	args = saashq._dict(args)

	ps = saashq.new_doc("Promotional Scheme")
	ps.name = "_Test Scheme"
	ps.append("items", {"item_code": "_Test Item"})

	ps.selling = 1
	ps.append(
		"price_discount_slabs",
		{
			"min_qty": 4,
			"validate_applied_rule": 0,
			"discount_percentage": 20,
			"rule_description": "Test",
		},
	)

	ps.company = "_Test Company"
	if args.applicable_for:
		ps.applicable_for = args.applicable_for
		ps.append(
			saashq.scrub(args.applicable_for),
			{saashq.scrub(args.applicable_for): args.get(saashq.scrub(args.applicable_for))},
		)

	ps.save()

	return ps
