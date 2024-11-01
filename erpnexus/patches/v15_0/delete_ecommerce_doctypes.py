import click
import saashq


def execute():
	if "webshop" in saashq.get_installed_apps():
		return

	if not saashq.db.table_exists("Website Item"):
		return

	doctypes = [
		"E Commerce Settings",
		"Website Item",
		"Recommended Items",
		"Item Review",
		"Wishlist Item",
		"Wishlist",
		"Website Offer",
		"Website Item Tabbed Section",
	]

	for doctype in doctypes:
		saashq.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"ECommerce is renamed and moved to a separate app"
		"Please install the app for ECommerce features: https://github.com/saashqdev/webshop",
		fg="yellow",
	)
