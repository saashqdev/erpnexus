# Copyright (c) 2020, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	if saashq.db.exists("DocType", "Issue"):
		saashq.reload_doc("support", "doctype", "issue")
		rename_status()


def rename_status():
	saashq.db.sql(
		"""
		UPDATE
			`tabIssue`
		SET
			status = 'On Hold'
		WHERE
			status = 'Hold'
	"""
	)
