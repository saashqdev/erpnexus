# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
		if saashq.db.exists("Report", report):
			saashq.delete_doc("Report", report)
