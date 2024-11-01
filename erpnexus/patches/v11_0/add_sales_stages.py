import saashq

from erpnexus.setup.setup_wizard.operations.install_fixtures import add_sale_stages


def execute():
	saashq.reload_doc("crm", "doctype", "sales_stage")

	saashq.local.lang = saashq.db.get_default("lang") or "en"

	add_sale_stages()
