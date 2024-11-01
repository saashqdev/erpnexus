# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase


class TestIssuePriority(IntegrationTestCase):
	def test_priorities(self):
		make_priorities()
		priorities = saashq.get_list("Issue Priority")

		for priority in priorities:
			self.assertIn(priority.name, ["Low", "Medium", "High"])


def make_priorities():
	insert_priority("Low")
	insert_priority("Medium")
	insert_priority("High")


def insert_priority(name):
	if not saashq.db.exists("Issue Priority", name):
		saashq.get_doc({"doctype": "Issue Priority", "name": name}).insert(ignore_permissions=True)
