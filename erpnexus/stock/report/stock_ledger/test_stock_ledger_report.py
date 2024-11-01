# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt

import saashq
from saashq.tests import IntegrationTestCase
from saashq.utils import add_days, today

from erpnexus.maintenance.doctype.maintenance_schedule.test_maintenance_schedule import (
	make_serial_item_with_serial,
)


class TestStockLedgerReeport(IntegrationTestCase):
	def setUp(self) -> None:
		make_serial_item_with_serial(self, "_Test Stock Report Serial Item")
		self.filters = saashq._dict(
			company="_Test Company",
			from_date=today(),
			to_date=add_days(today(), 30),
			item_code="_Test Stock Report Serial Item",
		)

	def tearDown(self) -> None:
		saashq.db.rollback()
