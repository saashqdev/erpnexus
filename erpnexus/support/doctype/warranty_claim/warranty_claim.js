// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

saashq.provide("erpnexus.support");

saashq.ui.form.on("Warranty Claim", {
	setup: (frm) => {
		frm.set_query("contact_person", erpnexus.queries.contact_query);
		frm.set_query("customer_address", erpnexus.queries.address_query);
		frm.set_query("customer", erpnexus.queries.customer);

		frm.set_query("serial_no", () => {
			let filters = {
				company: frm.doc.company,
			};

			if (frm.doc.item_code) {
				filters["item_code"] = frm.doc.item_code;
			}

			return { filters: filters };
		});

		frm.set_query("item_code", () => {
			return {
				filters: {
					disabled: 0,
				},
			};
		});
	},

	onload: (frm) => {
		if (!frm.doc.status) {
			frm.set_value("status", "Open");
		}
	},

	refresh: (frm) => {
		saashq.dynamic_link = {
			doc: frm.doc,
			fieldname: "customer",
			doctype: "Customer",
		};

		if (!frm.doc.__islocal && ["Open", "Work In Progress"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Maintenance Visit"), () => {
				saashq.model.open_mapped_doc({
					method: "erpnexus.support.doctype.warranty_claim.warranty_claim.make_maintenance_visit",
					frm: frm,
				});
			});
		}
	},

	customer: (frm) => {
		erpnexus.utils.get_party_details(frm);
	},

	customer_address: (frm) => {
		erpnexus.utils.get_address_display(frm);
	},

	contact_person: (frm) => {
		erpnexus.utils.get_contact_details(frm);
	},
});
