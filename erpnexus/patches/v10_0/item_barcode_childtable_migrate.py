# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("stock", "doctype", "item_barcode")
	if saashq.get_all("Item Barcode", limit=1):
		return
	if "barcode" not in saashq.db.get_table_columns("Item"):
		return

	items_barcode = saashq.db.sql("select name, barcode from tabItem where barcode is not null", as_dict=True)
	saashq.reload_doc("stock", "doctype", "item")

	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and "<" not in barcode:
			try:
				saashq.get_doc(
					{
						"idx": 0,
						"doctype": "Item Barcode",
						"barcode": barcode,
						"parenttype": "Item",
						"parent": item.name,
						"parentfield": "barcodes",
					}
				).insert()
			except (saashq.DuplicateEntryError, saashq.UniqueValidationError):
				continue
