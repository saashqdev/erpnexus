# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import saashq


def execute():
	navbar_settings = saashq.get_single("Navbar Settings")
	for item in navbar_settings.help_dropdown:
		if item.is_standard and item.route == "https://erpnexus.com/docs/user/manual":
			item.route = "https://docs.erpnexus.com/docs/v14/user/manual/en/introduction"

	navbar_settings.save()
