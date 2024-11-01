# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase


class TestQualityFeedback(IntegrationTestCase):
	def test_quality_feedback(self):
		template = saashq.get_doc(
			dict(
				doctype="Quality Feedback Template",
				template="Test Template",
				parameters=[dict(parameter="Test Parameter 1"), dict(parameter="Test Parameter 2")],
			)
		).insert()

		feedback = saashq.get_doc(
			dict(
				doctype="Quality Feedback",
				template=template.name,
				document_type="User",
				document_name=saashq.session.user,
			)
		).insert()

		self.assertEqual(template.parameters[0].parameter, feedback.parameters[0].parameter)

		feedback.delete()
		template.delete()
