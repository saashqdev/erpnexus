# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	if saashq.db.exists("DocType", "Scheduling Tool"):
		saashq.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
