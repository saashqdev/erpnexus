# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt

import saashq
from saashq.tests import IntegrationTestCase, UnitTestCase


class UnitTestWorkstationType(UnitTestCase):
	"""
	Unit tests for WorkstationType.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestWorkstationType(IntegrationTestCase):
	pass


def create_workstation_type(**args):
	args = saashq._dict(args)

	if workstation_type := saashq.db.exists("Workstation Type", args.workstation_type):
		return saashq.get_doc("Workstation Type", workstation_type)
	else:
		doc = saashq.new_doc("Workstation Type")
		doc.update(args)
		doc.insert()
		return doc
