import saashq
from saashq.model.utils.rename_field import rename_field


def execute():
	saashq.reload_doc("assets", "doctype", "asset")
	if saashq.db.has_column("Asset", "purchase_receipt_amount"):
		rename_field("Asset", "purchase_receipt_amount", "purchase_amount")
