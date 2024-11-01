# Copyright (c) 2019, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import saashq
from saashq.model.document import Document


class CommunicationMedium(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		from erpnexus.communication.doctype.communication_medium_timeslot.communication_medium_timeslot import (
			CommunicationMediumTimeslot,
		)

		catch_all: DF.Link | None
		communication_channel: DF.Literal
		communication_medium_type: DF.Literal["Voice", "Email", "Chat"]
		disabled: DF.Check
		provider: DF.Link | None
		timeslots: DF.Table[CommunicationMediumTimeslot]
	# end: auto-generated types

	pass
