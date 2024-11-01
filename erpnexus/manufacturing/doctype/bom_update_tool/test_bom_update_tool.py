# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import saashq
from saashq.tests import IntegrationTestCase, UnitTestCase, timeout

from erpnexus.manufacturing.doctype.bom_update_log.test_bom_update_log import (
	update_cost_in_all_boms_in_test,
)
from erpnexus.manufacturing.doctype.bom_update_tool.bom_update_tool import enqueue_replace_bom
from erpnexus.manufacturing.doctype.production_plan.test_production_plan import make_bom
from erpnexus.stock.doctype.item.test_item import create_item


class UnitTestBomUpdateTool(UnitTestCase):
	"""
	Unit tests for BomUpdateTool.
	Use this class for testing individual functions and methods.
	"""

	pass


EXTRA_TEST_RECORD_DEPENDENCIES = ["BOM"]


class TestBOMUpdateTool(IntegrationTestCase):
	"Test major functions run via BOM Update Tool."

	def tearDown(self):
		saashq.db.rollback()

	@timeout
	def test_replace_bom(self):
		current_bom = "BOM-_Test Item Home Desktop Manufactured-001"

		bom_doc = saashq.copy_doc(self.globalTestRecords["BOM"][0])
		bom_doc.items[1].item_code = "_Test Item"
		bom_doc.insert()

		boms = saashq._dict(current_bom=current_bom, new_bom=bom_doc.name)
		enqueue_replace_bom(boms=boms)

		self.assertFalse(saashq.db.exists("BOM Item", {"bom_no": current_bom, "docstatus": 1}))
		self.assertTrue(saashq.db.exists("BOM Item", {"bom_no": bom_doc.name, "docstatus": 1}))

	@timeout
	def test_bom_cost(self):
		for item in ["BOM Cost Test Item 1", "BOM Cost Test Item 2", "BOM Cost Test Item 3"]:
			item_doc = create_item(item, valuation_rate=100)
			if item_doc.valuation_rate != 100.00:
				saashq.db.set_value("Item", item_doc.name, "valuation_rate", 100)

		bom_no = saashq.db.get_value("BOM", {"item": "BOM Cost Test Item 1"}, "name")
		if not bom_no:
			doc = make_bom(
				item="BOM Cost Test Item 1",
				raw_materials=["BOM Cost Test Item 2", "BOM Cost Test Item 3"],
				currency="INR",
			)
		else:
			doc = saashq.get_doc("BOM", bom_no)

		self.assertEqual(doc.total_cost, 200)

		saashq.db.set_value("Item", "BOM Cost Test Item 2", "valuation_rate", 200)
		update_cost_in_all_boms_in_test()

		doc.load_from_db()
		self.assertEqual(doc.total_cost, 300)

		saashq.db.set_value("Item", "BOM Cost Test Item 2", "valuation_rate", 100)
		update_cost_in_all_boms_in_test()

		doc.load_from_db()
		self.assertEqual(doc.total_cost, 200)
