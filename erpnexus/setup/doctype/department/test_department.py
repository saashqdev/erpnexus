# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase

IGNORE_TEST_RECORD_DEPENDENCIES = ["Leave Block List"]


class TestDepartment(IntegrationTestCase):
	def test_remove_department_data(self):
		doc = create_department("Test Department")
		saashq.delete_doc("Department", doc.name)


def create_department(department_name, parent_department=None):
	doc = saashq.get_doc(
		{
			"doctype": "Department",
			"is_group": 0,
			"parent_department": parent_department,
			"department_name": department_name,
			"company": saashq.defaults.get_defaults().company,
		}
	).insert()

	return doc
