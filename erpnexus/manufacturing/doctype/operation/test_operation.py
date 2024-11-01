# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase


class TestOperation(IntegrationTestCase):
	pass


def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = saashq._dict(args)

	if not saashq.db.exists("Operation", args.operation):
		doc = saashq.get_doc(
			{"doctype": "Operation", "name": args.operation, "workstation": args.workstation}
		)
		doc.insert()
		return doc

	return saashq.get_doc("Operation", args.operation)
