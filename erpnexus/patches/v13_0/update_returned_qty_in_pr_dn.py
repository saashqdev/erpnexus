# Copyright (c) 2021, Saashq and Contributors
# License: GNU General Public License v3. See license.txt
import saashq

from erpnexus.controllers.status_updater import OverAllowanceError


def execute():
	saashq.reload_doc("stock", "doctype", "purchase_receipt")
	saashq.reload_doc("stock", "doctype", "purchase_receipt_item")
	saashq.reload_doc("stock", "doctype", "delivery_note")
	saashq.reload_doc("stock", "doctype", "delivery_note_item")
	saashq.reload_doc("stock", "doctype", "stock_settings")

	def update_from_return_docs(doctype):
		for return_doc in saashq.get_all(
			doctype, filters={"is_return": 1, "docstatus": 1, "return_against": ("!=", "")}
		):
			# Update original receipt/delivery document from return
			return_doc = saashq.get_cached_doc(doctype, return_doc.name)
			try:
				return_doc.update_prevdoc_status()
			except OverAllowanceError:
				saashq.db.rollback()
				continue

			return_against = saashq.get_doc(doctype, return_doc.return_against)
			return_against.update_billing_status()
			saashq.db.commit()

	# Set received qty in stock uom in PR, as returned qty is checked against it
	saashq.db.sql(
		""" update `tabPurchase Receipt Item`
		set received_stock_qty = received_qty * conversion_factor
		where docstatus = 1 """
	)

	for doctype in ("Purchase Receipt", "Delivery Note"):
		update_from_return_docs(doctype)
