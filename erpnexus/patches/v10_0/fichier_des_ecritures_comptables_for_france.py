# Copyright (c) 2018, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq

from erpnexus.setup.doctype.company.company import install_country_fixtures


def execute():
	saashq.reload_doc("regional", "report", "fichier_des_ecritures_comptables_[fec]")
	for d in saashq.get_all("Company", filters={"country": "France"}):
		install_country_fixtures(d.name)
