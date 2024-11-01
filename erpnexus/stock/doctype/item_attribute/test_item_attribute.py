# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt


import saashq
from saashq.tests import IntegrationTestCase, UnitTestCase

from erpnexus.stock.doctype.item_attribute.item_attribute import ItemAttributeIncrementError


class UnitTestItemAttribute(UnitTestCase):
	"""
	Unit tests for ItemAttribute.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestItemAttribute(IntegrationTestCase):
	def setUp(self):
		super().setUp()
		if saashq.db.exists("Item Attribute", "_Test_Length"):
			saashq.delete_doc("Item Attribute", "_Test_Length")

	def test_numeric_item_attribute(self):
		item_attribute = saashq.get_doc(
			{
				"doctype": "Item Attribute",
				"attribute_name": "_Test_Length",
				"numeric_values": 1,
				"from_range": 0.0,
				"to_range": 100.0,
				"increment": 0,
			}
		)

		self.assertRaises(ItemAttributeIncrementError, item_attribute.save)

		item_attribute.increment = 0.5
		item_attribute.save()
