# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt
import unittest

import saashq
from saashq.tests import IntegrationTestCase
from saashq.utils import random_string


class TestVehicle(IntegrationTestCase):
	def test_make_vehicle(self):
		vehicle = saashq.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": random_string(10).upper(),
				"make": "Maruti",
				"model": "PCM",
				"last_odometer": 5000,
				"acquisition_date": saashq.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234ABCD",
				"uom": "Litre",
				"vehicle_value": saashq.utils.flt(500000),
			}
		)
		vehicle.insert()

	def test_renaming_vehicle(self):
		license_plate = random_string(10).upper()

		vehicle = saashq.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": license_plate,
				"make": "Skoda",
				"model": "Slavia",
				"last_odometer": 5000,
				"acquisition_date": saashq.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234EFGH",
				"uom": "Litre",
				"vehicle_value": saashq.utils.flt(500000),
			}
		)
		vehicle.insert()

		new_license_plate = random_string(10).upper()
		saashq.rename_doc("Vehicle", license_plate, new_license_plate)

		self.assertEqual(
			new_license_plate, saashq.db.get_value("Vehicle", new_license_plate, "license_plate")
		)
