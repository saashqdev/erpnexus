# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt

import saashq
from saashq.tests import IntegrationTestCase, UnitTestCase

from erpnexus.stock.doctype.item.test_item import make_item
from erpnexus.stock.utils import _create_bin


class UnitTestBin(UnitTestCase):
	"""
	Unit tests for Bin.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestBin(IntegrationTestCase):
	def test_concurrent_inserts(self):
		"""Ensure no duplicates are possible in case of concurrent inserts"""
		item_code = "_TestConcurrentBin"
		make_item(item_code)
		warehouse = "_Test Warehouse - _TC"

		bin1 = saashq.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		bin1.insert()

		bin2 = saashq.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		with self.assertRaises(saashq.UniqueValidationError):
			bin2.insert()

		# util method should handle it
		bin = _create_bin(item_code, warehouse)
		self.assertEqual(bin.item_code, item_code)

		saashq.db.rollback()

	def test_index_exists(self):
		indexes = saashq.db.sql("show index from tabBin where Non_unique = 0", as_dict=1)
		if not any(index.get("Key_name") == "unique_item_warehouse" for index in indexes):
			self.fail("Expected unique index on item-warehouse")
