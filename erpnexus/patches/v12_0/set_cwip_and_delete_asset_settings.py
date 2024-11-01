import saashq
from saashq.utils import cint


def execute():
	"""Get 'Disable CWIP Accounting value' from Asset Settings, set it in 'Enable Capital Work in Progress Accounting' field
	in Company, delete Asset Settings"""

	if saashq.db.exists("DocType", "Asset Settings"):
		saashq.reload_doctype("Asset Category")
		cwip_value = saashq.db.get_single_value("Asset Settings", "disable_cwip_accounting")

		saashq.db.sql("""UPDATE `tabAsset Category` SET enable_cwip_accounting = %s""", cint(cwip_value))

		saashq.db.sql("""DELETE FROM `tabSingles` where doctype = 'Asset Settings'""")
		saashq.delete_doc_if_exists("DocType", "Asset Settings")
