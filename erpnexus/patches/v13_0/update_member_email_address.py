# Copyright (c) 2020, Saashq Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import saashq
from saashq.model.utils.rename_field import rename_field


def execute():
	"""add value to email_id column from email"""

	if saashq.db.has_column("Member", "email"):
		# Get all members
		for member in saashq.db.get_all("Member", pluck="name"):
			# Check if email_id already exists
			if not saashq.db.get_value("Member", member, "email_id"):
				# fetch email id from the user linked field email
				email = saashq.db.get_value("Member", member, "email")

				# Set the value for it
				saashq.db.set_value("Member", member, "email_id", email)

	if saashq.db.exists("DocType", "Membership Settings"):
		rename_field("Membership Settings", "enable_auto_invoicing", "enable_invoicing")
