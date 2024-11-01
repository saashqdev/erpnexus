# Copyright (c) 2020, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase


class TestPOSOpeningEntry(IntegrationTestCase):
	pass


def create_opening_entry(pos_profile, user):
	entry = saashq.new_doc("POS Opening Entry")
	entry.pos_profile = pos_profile.name
	entry.user = user
	entry.company = pos_profile.company
	entry.period_start_date = saashq.utils.get_datetime()

	balance_details = []
	for d in pos_profile.payments:
		balance_details.append(saashq._dict({"mode_of_payment": d.mode_of_payment}))

	entry.set("balance_details", balance_details)
	entry.submit()

	return entry.as_dict()
