import unittest

import saashq
from saashq.tests import IntegrationTestCase

from erpnexus import encode_company_abbr

EXTRA_TEST_RECORD_DEPENDENCIES = ["Company"]


class TestInit(IntegrationTestCase):
	def test_encode_company_abbr(self):
		abbr = "NFECT"

		names = [
			"Warehouse Name",
			"ERPNexus Foundation India",
			f"Gold - Member - {abbr}",
			f" - {abbr}",
			"ERPNexus - Foundation - India",
			f"ERPNexus Foundation India - {abbr}",
			f"No-Space-{abbr}",
			"- Warehouse",
		]

		expected_names = [
			f"Warehouse Name - {abbr}",
			f"ERPNexus Foundation India - {abbr}",
			f"Gold - Member - {abbr}",
			f" - {abbr}",
			f"ERPNexus - Foundation - India - {abbr}",
			f"ERPNexus Foundation India - {abbr}",
			f"No-Space-{abbr} - {abbr}",
			f"- Warehouse - {abbr}",
		]

		for i in range(len(names)):
			enc_name = encode_company_abbr(names[i], abbr=abbr)
			self.assertTrue(
				enc_name == expected_names[i],
				f"{enc_name} is not same as {expected_names[i]}",
			)

	def test_translation_files(self):
		from saashq.tests.test_translate import verify_translation_files

		verify_translation_files("erpnexus")

	def test_patches(self):
		from saashq.tests.test_patches import check_patch_files

		check_patch_files("erpnexus")
