# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase


class TestCostCenter(IntegrationTestCase):
	def test_cost_center_creation_against_child_node(self):
		cost_center = saashq.get_doc(
			{
				"doctype": "Cost Center",
				"cost_center_name": "_Test Cost Center 3",
				"parent_cost_center": "_Test Cost Center 2 - _TC",
				"is_group": 0,
				"company": "_Test Company",
			}
		)

		self.assertRaises(saashq.ValidationError, cost_center.save)


def create_cost_center(**args):
	args = saashq._dict(args)
	if args.cost_center_name:
		company = args.company or "_Test Company"
		company_abbr = saashq.db.get_value("Company", company, "abbr")
		cc_name = args.cost_center_name + " - " + company_abbr
		if not saashq.db.exists("Cost Center", cc_name):
			cc = saashq.new_doc("Cost Center")
			cc.company = args.company or "_Test Company"
			cc.cost_center_name = args.cost_center_name
			cc.is_group = args.is_group or 0
			cc.parent_cost_center = args.parent_cost_center or "_Test Company - _TC"
			cc.insert()
