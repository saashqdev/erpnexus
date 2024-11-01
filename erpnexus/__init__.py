import functools
import inspect

import saashq
from saashq.utils.user import is_website_user

__version__ = "16.0.0-dev"


def get_default_company(user=None):
	"""Get default company for user"""
	from saashq.defaults import get_user_default_as_list

	if not user:
		user = saashq.session.user

	companies = get_user_default_as_list("company", user)
	if companies:
		default_company = companies[0]
	else:
		default_company = saashq.db.get_single_value("Global Defaults", "default_company")

	return default_company


def get_default_currency():
	"""Returns the currency of the default company"""
	company = get_default_company()
	if company:
		return saashq.get_cached_value("Company", company, "default_currency")


def get_default_cost_center(company):
	"""Returns the default cost center of the company"""
	if not company:
		return None

	if not saashq.flags.company_cost_center:
		saashq.flags.company_cost_center = {}
	if company not in saashq.flags.company_cost_center:
		saashq.flags.company_cost_center[company] = saashq.get_cached_value("Company", company, "cost_center")
	return saashq.flags.company_cost_center[company]


def get_company_currency(company):
	"""Returns the default company currency"""
	if not saashq.flags.company_currency:
		saashq.flags.company_currency = {}
	if company not in saashq.flags.company_currency:
		saashq.flags.company_currency[company] = saashq.db.get_value(
			"Company", company, "default_currency", cache=True
		)
	return saashq.flags.company_currency[company]


def set_perpetual_inventory(enable=1, company=None):
	if not company:
		company = "_Test Company" if saashq.flags.in_test else get_default_company()

	company = saashq.get_doc("Company", company)
	company.enable_perpetual_inventory = enable
	company.save()


def encode_company_abbr(name, company=None, abbr=None):
	"""Returns name encoded with company abbreviation"""
	company_abbr = abbr or saashq.get_cached_value("Company", company, "abbr")
	parts = name.rsplit(" - ", 1)

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)


def is_perpetual_inventory_enabled(company):
	if not company:
		company = "_Test Company" if saashq.flags.in_test else get_default_company()

	if not hasattr(saashq.local, "enable_perpetual_inventory"):
		saashq.local.enable_perpetual_inventory = {}

	if company not in saashq.local.enable_perpetual_inventory:
		saashq.local.enable_perpetual_inventory[company] = (
			saashq.get_cached_value("Company", company, "enable_perpetual_inventory") or 0
		)

	return saashq.local.enable_perpetual_inventory[company]


def get_default_finance_book(company=None):
	if not company:
		company = get_default_company()

	if not hasattr(saashq.local, "default_finance_book"):
		saashq.local.default_finance_book = {}

	if company not in saashq.local.default_finance_book:
		saashq.local.default_finance_book[company] = saashq.get_cached_value(
			"Company", company, "default_finance_book"
		)

	return saashq.local.default_finance_book[company]


def get_party_account_type(party_type):
	if not hasattr(saashq.local, "party_account_types"):
		saashq.local.party_account_types = {}

	if party_type not in saashq.local.party_account_types:
		saashq.local.party_account_types[party_type] = (
			saashq.db.get_value("Party Type", party_type, "account_type") or ""
		)

	return saashq.local.party_account_types[party_type]


def get_region(company=None):
	"""Return the default country based on flag, company or global settings

	You can also set global company flag in `saashq.flags.company`
	"""

	if not company:
		company = saashq.local.flags.company

	if company:
		return saashq.get_cached_value("Company", company, "country")

	return saashq.flags.country or saashq.get_system_settings("country")


def allow_regional(fn):
	"""Decorator to make a function regionally overridable

	Example:
	@erpnexus.allow_regional
	def myfunction():
	  pass"""

	@functools.wraps(fn)
	def caller(*args, **kwargs):
		overrides = saashq.get_hooks("regional_overrides", {}).get(get_region())
		function_path = f"{inspect.getmodule(fn).__name__}.{fn.__name__}"

		if not overrides or function_path not in overrides:
			return fn(*args, **kwargs)

		# Priority given to last installed app
		return saashq.get_attr(overrides[function_path][-1])(*args, **kwargs)

	return caller


def check_app_permission():
	if saashq.session.user == "Administrator":
		return True

	if is_website_user():
		return False

	return True
