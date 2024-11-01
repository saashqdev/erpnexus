# Copyright (c) 2020, Saashq Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import saashq
from apiclient.discovery import build
from saashq import _
from saashq.model.document import Document


class VideoSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from saashq.types import DF

		api_key: DF.Data | None
		enable_youtube_tracking: DF.Check
		frequency: DF.Literal["30 mins", "1 hr", "6 hrs", "Daily"]
	# end: auto-generated types

	def validate(self):
		self.validate_youtube_api_key()

	def validate_youtube_api_key(self):
		if self.enable_youtube_tracking and self.api_key:
			try:
				build("youtube", "v3", developerKey=self.api_key)
			except Exception:
				title = _("Failed to Authenticate the API key.")
				self.log_error("Failed to authenticate API key")
				saashq.throw(title + " Please check the error logs.", title=_("Invalid Credentials"))
