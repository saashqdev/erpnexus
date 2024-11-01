# Copyright (c) 2022, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import saashq
from saashq.model.document import Document
from saashq.utils import flt


class WorkstationType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		description: DF.SmallText | None
		hour_rate: DF.Currency
		hour_rate_consumable: DF.Currency
		hour_rate_electricity: DF.Currency
		hour_rate_labour: DF.Currency
		hour_rate_rent: DF.Currency
		workstation_type: DF.Data
	# end: auto-generated types

	def before_save(self):
		self.set_hour_rate()

	def set_hour_rate(self):
		self.hour_rate = (
			flt(self.hour_rate_labour)
			+ flt(self.hour_rate_electricity)
			+ flt(self.hour_rate_consumable)
			+ flt(self.hour_rate_rent)
		)


def get_workstations(workstation_type):
	workstations = saashq.get_all(
		"Workstation", filters={"workstation_type": workstation_type}, order_by="creation"
	)

	return [workstation.name for workstation in workstations]
