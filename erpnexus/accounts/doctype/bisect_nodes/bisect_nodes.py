# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import saashq
from saashq.model.document import Document


class BisectNodes(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		balance_sheet_summary: DF.Float
		difference: DF.Float
		generated: DF.Check
		left_child: DF.Link | None
		name: DF.Int | None
		period_from_date: DF.Datetime | None
		period_to_date: DF.Datetime | None
		profit_loss_summary: DF.Float
		right_child: DF.Link | None
		root: DF.Link | None
	# end: auto-generated types

	pass
