# Copyright (c) 2018, Saashq and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase

from ..quality_goal.test_quality_goal import get_quality_goal
from .quality_review import review


class TestQualityReview(IntegrationTestCase):
	def test_review_creation(self):
		quality_goal = get_quality_goal()
		review()

		# check if review exists
		quality_review = saashq.get_doc("Quality Review", dict(goal=quality_goal.name))
		self.assertEqual(quality_goal.objectives[0].target, quality_review.reviews[0].target)
		quality_review.delete()

		quality_goal.delete()
