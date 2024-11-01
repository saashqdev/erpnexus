import click
import saashq
from saashq import _
from saashq.desk.doctype.notification_log.notification_log import make_notification_logs
from saashq.utils.user import get_system_managers

SETTINGS_DOCTYPE = "Exotel Settings"


def execute():
	if "exotel_integration" in saashq.get_installed_apps():
		return

	try:
		exotel = saashq.get_doc(SETTINGS_DOCTYPE)
		if exotel.enabled:
			notify_existing_users()

		saashq.delete_doc("DocType", SETTINGS_DOCTYPE)
	except Exception:
		saashq.log_error("Failed to remove Exotel Integration.")


def notify_existing_users():
	click.secho(
		"Exotel integration is moved to a separate app and will be removed from ERPNexus in version-15.\n"
		"Please install the app to continue using the integration: https://github.com/saashqdev/exotel_integration",
		fg="yellow",
	)

	notification = {
		"subject": _(
			"WARNING: Exotel app has been separated from ERPNexus, please install the app to continue using Exotel integration."
		),
		"type": "Alert",
	}
	make_notification_logs(notification, get_system_managers(only_name=True))
