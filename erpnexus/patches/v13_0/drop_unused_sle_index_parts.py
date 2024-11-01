import saashq

from erpnexus.stock.doctype.stock_ledger_entry.stock_ledger_entry import on_doctype_update


def execute():
	try:
		saashq.db.sql_ddl("ALTER TABLE `tabStock Ledger Entry` DROP INDEX `posting_sort_index`")
	except Exception:
		saashq.log_error("Failed to drop index")
		return

	# Recreate indexes
	on_doctype_update()
