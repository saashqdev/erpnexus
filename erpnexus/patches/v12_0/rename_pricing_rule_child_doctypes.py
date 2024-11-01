# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq

doctypes = {
	"Price Discount Slab": "Promotional Scheme Price Discount",
	"Product Discount Slab": "Promotional Scheme Product Discount",
	"Apply Rule On Item Code": "Pricing Rule Item Code",
	"Apply Rule On Item Group": "Pricing Rule Item Group",
	"Apply Rule On Brand": "Pricing Rule Brand",
}


def execute():
	for old_doc, new_doc in doctypes.items():
		if not saashq.db.table_exists(new_doc) and saashq.db.table_exists(old_doc):
			saashq.rename_doc("DocType", old_doc, new_doc)
			saashq.reload_doc("accounts", "doctype", saashq.scrub(new_doc))
			saashq.delete_doc("DocType", old_doc)
