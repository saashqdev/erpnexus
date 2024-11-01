import saashq
from saashq.utils import cint


def execute():
	saashq.reload_doc("erpnexus_integrations", "doctype", "woocommerce_settings")
	doc = saashq.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)
