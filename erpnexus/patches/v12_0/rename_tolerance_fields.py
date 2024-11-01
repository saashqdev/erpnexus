import saashq
from saashq.model.utils.rename_field import rename_field


def execute():
	saashq.reload_doc("stock", "doctype", "item")
	saashq.reload_doc("stock", "doctype", "stock_settings")
	saashq.reload_doc("accounts", "doctype", "accounts_settings")

	rename_field("Stock Settings", "tolerance", "over_delivery_receipt_allowance")
	rename_field("Item", "tolerance", "over_delivery_receipt_allowance")

	qty_allowance = saashq.db.get_single_value("Stock Settings", "over_delivery_receipt_allowance")
	saashq.db.set_single_value("Accounts Settings", "over_delivery_receipt_allowance", qty_allowance)

	saashq.db.sql("update tabItem set over_billing_allowance=over_delivery_receipt_allowance")
