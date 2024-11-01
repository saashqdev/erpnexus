# Copyright (c) 2020, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq
from saashq.model.utils.rename_field import rename_field


def execute():
	saashq.reload_doc("support", "doctype", "sla_fulfilled_on_status")
	saashq.reload_doc("support", "doctype", "service_level_agreement")
	if saashq.db.has_column("Service Level Agreement", "enable"):
		rename_field("Service Level Agreement", "enable", "enabled")

	for sla in saashq.get_all("Service Level Agreement"):
		agreement = saashq.get_doc("Service Level Agreement", sla.name)
		agreement.db_set("document_type", "Issue")
		agreement.reload()
		agreement.apply_sla_for_resolution = 1
		agreement.append("sla_fulfilled_on", {"status": "Resolved"})
		agreement.append("sla_fulfilled_on", {"status": "Closed"})
		agreement.save()
