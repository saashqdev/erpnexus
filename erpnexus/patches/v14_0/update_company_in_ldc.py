# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import saashq

from erpnexus import get_default_company


def execute():
	company = get_default_company()
	if company:
		for d in saashq.get_all("Lower Deduction Certificate", pluck="name"):
			saashq.db.set_value("Lower Deduction Certificate", d, "company", company, update_modified=False)
