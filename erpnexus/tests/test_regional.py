import unittest

import saashq
from saashq.tests import IntegrationTestCase

import erpnexus


@erpnexus.allow_regional
def test_method():
	return "original"


class TestInit(IntegrationTestCase):
	def test_regional_overrides(self):
		saashq.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")
