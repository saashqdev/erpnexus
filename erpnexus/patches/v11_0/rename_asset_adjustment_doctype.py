# Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	if saashq.db.table_exists("Asset Adjustment") and not saashq.db.table_exists("Asset Value Adjustment"):
		saashq.rename_doc("DocType", "Asset Adjustment", "Asset Value Adjustment", force=True)
		saashq.reload_doc("assets", "doctype", "asset_value_adjustment")
