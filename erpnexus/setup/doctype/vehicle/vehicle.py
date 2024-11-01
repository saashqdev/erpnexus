# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq import _
from saashq.model.document import Document
from saashq.utils import getdate


class Vehicle(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		acquisition_date: DF.Date | None
		amended_from: DF.Link | None
		carbon_check_date: DF.Date | None
		chassis_no: DF.Data | None
		color: DF.Data | None
		doors: DF.Int
		employee: DF.Link | None
		end_date: DF.Date | None
		fuel_type: DF.Literal["Petrol", "Diesel", "Natural Gas", "Electric"]
		insurance_company: DF.Data | None
		last_odometer: DF.Int
		license_plate: DF.Data
		location: DF.Data | None
		make: DF.Data
		model: DF.Data
		policy_no: DF.Data | None
		start_date: DF.Date | None
		uom: DF.Link
		vehicle_value: DF.Currency
		wheels: DF.Int
	# end: auto-generated types

	def validate(self):
		if getdate(self.start_date) > getdate(self.end_date):
			saashq.throw(_("Insurance Start date should be less than Insurance End date"))
		if getdate(self.carbon_check_date) > getdate():
			saashq.throw(_("Last carbon check date cannot be a future date"))
