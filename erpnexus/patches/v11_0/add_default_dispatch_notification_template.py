import os

import saashq
from saashq import _


def execute():
	saashq.reload_doc("email", "doctype", "email_template")
	saashq.reload_doc("stock", "doctype", "delivery_settings")

	if not saashq.db.exists("Email Template", _("Dispatch Notification")):
		base_path = saashq.get_app_path("erpnexus", "stock", "doctype")
		response = saashq.read_file(
			os.path.join(base_path, "delivery_trip/dispatch_notification_template.html")
		)

		saashq.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Dispatch Notification"),
				"response": response,
				"subject": _("Your order is out for delivery!"),
				"owner": saashq.session.user,
			}
		).insert(ignore_permissions=True)

	delivery_settings = saashq.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.flags.ignore_links = True
	delivery_settings.save()
