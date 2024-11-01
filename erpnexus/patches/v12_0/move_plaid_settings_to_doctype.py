# Copyright (c) 2017, Saashq and Contributors
# License: GNU General Public License v3. See license.txt


import saashq


def execute():
	saashq.reload_doc("erpnexus_integrations", "doctype", "plaid_settings")
	plaid_settings = saashq.get_single("Plaid Settings")
	if plaid_settings.enabled:
		if not (saashq.conf.plaid_client_id and saashq.conf.plaid_env and saashq.conf.plaid_secret):
			plaid_settings.enabled = 0
		else:
			plaid_settings.update(
				{
					"plaid_client_id": saashq.conf.plaid_client_id,
					"plaid_env": saashq.conf.plaid_env,
					"plaid_secret": saashq.conf.plaid_secret,
				}
			)
		plaid_settings.flags.ignore_mandatory = True
		plaid_settings.save()
