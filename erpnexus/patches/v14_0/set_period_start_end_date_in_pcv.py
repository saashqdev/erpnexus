# Copyright (c) 2023, Saashq Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import saashq


def execute():
	# nosemgrep
	saashq.db.sql(
		"""
		UPDATE `tabPeriod Closing Voucher`
		SET
			period_start_date = (select year_start_date from `tabFiscal Year` where name = fiscal_year),
			period_end_date = posting_date
	"""
	)
