# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import saashq


def create_designation(**args):
	args = saashq._dict(args)
	if saashq.db.exists("Designation", args.designation_name or "_Test designation"):
		return saashq.get_doc("Designation", args.designation_name or "_Test designation")

	designation = saashq.get_doc(
		{
			"doctype": "Designation",
			"designation_name": args.designation_name or "_Test designation",
			"description": args.description or "_Test description",
		}
	)
	designation.save()
	return designation
