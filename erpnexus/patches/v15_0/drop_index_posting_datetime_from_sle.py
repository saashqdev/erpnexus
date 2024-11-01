import click
import saashq


def execute():
	table = "tabStock Ledger Entry"
	index = "posting_datetime_creation_index"

	if not saashq.db.has_index(table, index):
		return

	try:
		saashq.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
		click.echo(f"✓ dropped {index} index from {table}")
	except Exception:
		saashq.log_error("Failed to drop index")
