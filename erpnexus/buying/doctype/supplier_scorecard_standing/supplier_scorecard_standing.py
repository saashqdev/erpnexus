# Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from saashq.model.document import Document


class SupplierScorecardStanding(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		employee_link: DF.Link | None
		max_grade: DF.Percent
		min_grade: DF.Percent
		notify_employee: DF.Check
		notify_supplier: DF.Check
		prevent_pos: DF.Check
		prevent_rfqs: DF.Check
		standing_color: DF.Literal["Blue", "Purple", "Green", "Yellow", "Orange", "Red"]
		standing_name: DF.Data | None
		warn_pos: DF.Check
		warn_rfqs: DF.Check
	# end: auto-generated types

	pass


@saashq.whitelist()
def get_scoring_standing(standing_name):
	standing = saashq.get_doc("Supplier Scorecard Standing", standing_name)

	return standing


@saashq.whitelist()
def get_standings_list():
	standings = saashq.db.sql(
		"""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Standing` scs""",
		{},
		as_dict=1,
	)

	return standings
