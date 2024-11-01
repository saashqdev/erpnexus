import click
import saashq


def execute():
	if (
		not saashq.db.exists("Company", {"country": "India"})
		or "india_compliance" in saashq.get_installed_apps()
	):
		return

	click.secho(
		"India-specific regional features have been moved to a separate app"
		" and will be removed from ERPNexus in Version 14."
		" Please install India Compliance after upgrading to Version 14:\n"
		"https://github.com/resilient-tech/india-compliance",
		fg="yellow",
	)
