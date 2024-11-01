import saashq


def execute():
	install_apps = saashq.get_installed_apps()
	if "erpnexus_datev_uo" in install_apps or "erpnexus_datev" in install_apps:
		return

	# doctypes
	saashq.delete_doc("DocType", "DATEV Settings", ignore_missing=True, force=True)

	# reports
	saashq.delete_doc("Report", "DATEV", ignore_missing=True, force=True)
