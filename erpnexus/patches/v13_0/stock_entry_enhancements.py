# Copyright(c) 2020, Saashq Technologies Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt


import saashq


def execute():
	saashq.reload_doc("stock", "doctype", "stock_entry")
	if saashq.db.has_column("Stock Entry", "add_to_transit"):
		saashq.db.sql(
			"""
            UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer',
            add_to_transit = 1 WHERE stock_entry_type = 'Send to Warehouse'
            """
		)

		saashq.db.sql(
			"""UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer'
            WHERE stock_entry_type = 'Receive at Warehouse'
            """
		)

		saashq.reload_doc("stock", "doctype", "warehouse_type")
		if not saashq.db.exists("Warehouse Type", "Transit"):
			doc = saashq.new_doc("Warehouse Type")
			doc.name = "Transit"
			doc.insert()

		saashq.reload_doc("stock", "doctype", "stock_entry_type")
		saashq.delete_doc_if_exists("Stock Entry Type", "Send to Warehouse")
		saashq.delete_doc_if_exists("Stock Entry Type", "Receive at Warehouse")
