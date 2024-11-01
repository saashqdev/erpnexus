// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.cscript.tax_table = "Purchase Taxes and Charges";
erpnexus.accounts.taxes.setup_tax_validations("Purchase Taxes and Charges Template");
erpnexus.accounts.taxes.setup_tax_filters("Purchase Taxes and Charges");

saashq.ui.form.on("Purchase Taxes and Charges", {
	add_deduct_tax(doc, cdt, cdn) {
		let d = locals[cdt][cdn];

		if (!d.category && d.add_deduct_tax) {
			saashq.msgprint(__("Please select Category first"));
			d.add_deduct_tax = "";
		} else if (d.category != "Total" && d.add_deduct_tax == "Deduct") {
			saashq.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
			d.add_deduct_tax = "";
		}
		refresh_field("add_deduct_tax", d.name, "taxes");
	},

	category(doc, cdt, cdn) {
		let d = locals[cdt][cdn];

		if (d.category != "Total" && d.add_deduct_tax == "Deduct") {
			saashq.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
			d.add_deduct_tax = "";
		}
		refresh_field("add_deduct_tax", d.name, "taxes");
	},
});
