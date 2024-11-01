import click
import saashq


def execute():
	if "ksa" in saashq.get_installed_apps():
		return
	click.secho(
		"Region Saudi Arabia(KSA) is moved to a separate app\n"
		"Please install the app to continue using the KSA Features: https://github.com/8848digital/KSA",
		fg="yellow",
	)
