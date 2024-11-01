import click
import saashq


def execute():
	if "taxjar_integration" in saashq.get_installed_apps():
		return

	doctypes = ["TaxJar Settings", "TaxJar Nexus", "Product Tax Category"]
	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"Taxjar Integration is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/saashqdev/taxjar_integration",
		fg="yellow",
	)
