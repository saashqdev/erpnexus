import saashq
from saashq import _


def execute():
	saashq.reload_doctype("Selling Settings")
	selling_settings = saashq.get_single("Selling Settings")

	if selling_settings.customer_group in (_("All Customer Groups"), "All Customer Groups"):
		selling_settings.customer_group = None

	if selling_settings.territory in (_("All Territories"), "All Territories"):
		selling_settings.territory = None

	selling_settings.flags.ignore_mandatory = True
	selling_settings.save(ignore_permissions=True)
