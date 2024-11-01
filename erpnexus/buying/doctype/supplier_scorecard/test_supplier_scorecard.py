# Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and Contributors
# See license.txt


import saashq
from saashq.tests import IntegrationTestCase, UnitTestCase


class UnitTestSupplierScorecard(UnitTestCase):
	"""
	Unit tests for SupplierScorecard.
	Use this class for testing individual functions and methods.
	"""

	pass


class TestSupplierScorecard(IntegrationTestCase):
	def test_create_scorecard(self):
		doc = make_supplier_scorecard().insert()
		self.assertEqual(doc.name, valid_scorecard[0].get("supplier"))

	def test_criteria_weight(self):
		delete_test_scorecards()
		my_doc = make_supplier_scorecard()
		for d in my_doc.criteria:
			d.weight = 0
		self.assertRaises(saashq.ValidationError, my_doc.insert)


def make_supplier_scorecard():
	my_doc = saashq.get_doc(valid_scorecard[0])

	# Make sure the criteria exist (making them)
	for d in valid_scorecard[0].get("criteria"):
		if not saashq.db.exists("Supplier Scorecard Criteria", d.get("criteria_name")):
			d["doctype"] = "Supplier Scorecard Criteria"
			d["name"] = d.get("criteria_name")
			my_criteria = saashq.get_doc(d)
			my_criteria.insert()
	return my_doc


def delete_test_scorecards():
	my_doc = make_supplier_scorecard()
	if saashq.db.exists("Supplier Scorecard", my_doc.name):
		# Delete all the periods, then delete the scorecard
		saashq.db.sql(
			"""delete from `tabSupplier Scorecard Period` where scorecard = %(scorecard)s""",
			{"scorecard": my_doc.name},
		)
		saashq.db.sql(
			"""delete from `tabSupplier Scorecard Scoring Criteria` where parenttype = 'Supplier Scorecard Period'"""
		)
		saashq.db.sql(
			"""delete from `tabSupplier Scorecard Scoring Standing` where parenttype = 'Supplier Scorecard Period'"""
		)
		saashq.db.sql(
			"""delete from `tabSupplier Scorecard Scoring Variable` where parenttype = 'Supplier Scorecard Period'"""
		)
		saashq.delete_doc(my_doc.doctype, my_doc.name)


valid_scorecard = [
	{
		"standings": [
			{
				"min_grade": 0.0,
				"name": "Very Poor",
				"prevent_rfqs": 1,
				"notify_supplier": 0,
				"doctype": "Supplier Scorecard Scoring Standing",
				"max_grade": 30.0,
				"prevent_pos": 1,
				"warn_pos": 0,
				"warn_rfqs": 0,
				"standing_color": "Red",
				"notify_employee": 0,
				"standing_name": "Very Poor",
				"parenttype": "Supplier Scorecard",
				"parentfield": "standings",
			},
			{
				"min_grade": 30.0,
				"name": "Poor",
				"prevent_rfqs": 1,
				"notify_supplier": 0,
				"doctype": "Supplier Scorecard Scoring Standing",
				"max_grade": 50.0,
				"prevent_pos": 0,
				"warn_pos": 0,
				"warn_rfqs": 0,
				"standing_color": "Red",
				"notify_employee": 0,
				"standing_name": "Poor",
				"parenttype": "Supplier Scorecard",
				"parentfield": "standings",
			},
			{
				"min_grade": 50.0,
				"name": "Average",
				"prevent_rfqs": 0,
				"notify_supplier": 0,
				"doctype": "Supplier Scorecard Scoring Standing",
				"max_grade": 80.0,
				"prevent_pos": 0,
				"warn_pos": 0,
				"warn_rfqs": 0,
				"standing_color": "Green",
				"notify_employee": 0,
				"standing_name": "Average",
				"parenttype": "Supplier Scorecard",
				"parentfield": "standings",
			},
			{
				"min_grade": 80.0,
				"name": "Excellent",
				"prevent_rfqs": 0,
				"notify_supplier": 0,
				"doctype": "Supplier Scorecard Scoring Standing",
				"max_grade": 100.0,
				"prevent_pos": 0,
				"warn_pos": 0,
				"warn_rfqs": 0,
				"standing_color": "Blue",
				"notify_employee": 0,
				"standing_name": "Excellent",
				"parenttype": "Supplier Scorecard",
				"parentfield": "standings",
			},
		],
		"prevent_pos": 0,
		"period": "Per Month",
		"doctype": "Supplier Scorecard",
		"warn_pos": 0,
		"warn_rfqs": 0,
		"notify_supplier": 0,
		"criteria": [
			{
				"weight": 100.0,
				"doctype": "Supplier Scorecard Scoring Criteria",
				"criteria_name": "Delivery",
				"formula": "100",
			}
		],
		"supplier": "_Test Supplier",
		"name": "_Test Supplier",
		"weighting_function": "{total_score} * max( 0, min ( 1 , (12 - {period_number}) / 12) )",
	}
]
