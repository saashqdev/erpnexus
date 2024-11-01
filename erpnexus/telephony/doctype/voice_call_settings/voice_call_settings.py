# Copyright (c) 2020, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import saashq
from saashq.model.document import Document


class VoiceCallSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		agent_busy_message: DF.Data | None
		agent_unavailable_message: DF.Data | None
		call_receiving_device: DF.Literal["Computer", "Phone"]
		greeting_message: DF.Data | None
		user: DF.Link
	# end: auto-generated types

	pass
