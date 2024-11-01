# Copyright (c) 2018, Saashq and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase


class TestQualityGoal(IntegrationTestCase):
	def test_quality_goal(self):
		# no code, just a basic sanity check
		goal = get_quality_goal()
		self.assertTrue(goal)
		goal.delete()


def get_quality_goal():
	return saashq.get_doc(
		dict(
			doctype="Quality Goal",
			goal="Test Quality Module",
			frequency="Daily",
			objectives=[dict(objective="Check test cases", target="100", uom="Percent")],
		)
	).insert()