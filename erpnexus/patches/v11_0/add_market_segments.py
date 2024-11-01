import saashq

from erpnexus.setup.setup_wizard.operations.install_fixtures import add_market_segments


def execute():
	saashq.reload_doc("crm", "doctype", "market_segment")

	saashq.local.lang = saashq.db.get_default("lang") or "en"

	add_market_segments()
