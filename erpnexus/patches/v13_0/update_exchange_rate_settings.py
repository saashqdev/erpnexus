import saashq

from erpnexus.setup.install import setup_currency_exchange


def execute():
	saashq.reload_doc("accounts", "doctype", "currency_exchange_settings")
	setup_currency_exchange()
