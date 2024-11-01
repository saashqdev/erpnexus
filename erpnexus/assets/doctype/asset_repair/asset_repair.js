// Copyright (c) 2017, Saashq Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

saashq.ui.form.on("Asset Repair", {
	setup: function (frm) {
		frm.fields_dict.cost_center.get_query = function (doc) {
			return {
				filters: {
					is_group: 0,
					company: doc.company,
				},
			};
		};

		frm.fields_dict.project.get_query = function (doc) {
			return {
				filters: {
					company: doc.company,
				},
			};
		};

		frm.set_query("asset", function () {
			return {
				filters: {
					company: frm.doc.company,
					docstatus: 1,
				},
			};
		});

		frm.set_query("purchase_invoice", "invoices", function () {
			return {
				query: "erpnexus.assets.doctype.asset_repair.asset_repair.get_purchase_invoice",
				filters: {
					company: frm.doc.company,
					docstatus: 1,
				},
			};
		});

		frm.set_query("warehouse", "stock_items", function () {
			return {
				filters: {
					is_group: 0,
					company: frm.doc.company,
				},
			};
		});

		frm.set_query("serial_and_batch_bundle", "stock_items", (doc, cdt, cdn) => {
			let row = locals[cdt][cdn];
			return {
				filters: {
					item_code: row.item_code,
					voucher_type: doc.doctype,
					voucher_no: ["in", [doc.name, ""]],
					is_cancelled: 0,
				},
			};
		});

		frm.set_query("expense_account", "invoices", function () {
			return {
				filters: {
					company: frm.doc.company,
					is_group: ["=", 0],
					report_type: ["=", "Profit and Loss"],
				},
			};
		});
	},

	refresh: function (frm) {
		if (frm.doc.docstatus) {
			frm.add_custom_button(__("View General Ledger"), function () {
				saashq.route_options = {
					voucher_no: frm.doc.name,
				};
				saashq.set_route("query-report", "General Ledger");
			});
		}

		let sbb_field = frm.get_docfield("stock_items", "serial_and_batch_bundle");
		if (sbb_field) {
			sbb_field.get_route_options_for_new_doc = (row) => {
				return {
					item_code: row.doc.item_code,
					voucher_type: frm.doc.doctype,
				};
			};
		}
	},

	repair_status: (frm) => {
		if (frm.doc.completion_date && frm.doc.repair_status == "Completed") {
			saashq.call({
				method: "erpnexus.assets.doctype.asset_repair.asset_repair.get_downtime",
				args: {
					failure_date: frm.doc.failure_date,
					completion_date: frm.doc.completion_date,
				},
				callback: function (r) {
					if (r.message) {
						frm.set_value("downtime", r.message + " Hrs");
					}
				},
			});
		}

		if (frm.doc.repair_status == "Completed" && !frm.doc.completion_date) {
			frm.set_value("completion_date", saashq.datetime.now_datetime());
		}
	},

	stock_items_on_form_rendered() {
		erpnexus.setup_serial_or_batch_no();
	},

	stock_consumption: function (frm) {
		if (!frm.doc.stock_consumption) {
			frm.clear_table("stock_items");
			frm.refresh_field("stock_items");
		}
	},

	purchase_invoice: function (frm) {
		if (frm.doc.purchase_invoice) {
			saashq.call({
				method: "saashq.client.get_value",
				args: {
					doctype: "Purchase Invoice",
					fieldname: "base_net_total",
					filters: { name: frm.doc.purchase_invoice },
				},
				callback: function (r) {
					if (r.message) {
						frm.set_value("repair_cost", r.message.base_net_total);
					}
				},
			});
		} else {
			frm.set_value("repair_cost", 0);
		}
	},
});

saashq.ui.form.on("Asset Repair Consumed Item", {
	warehouse: function (frm, cdt, cdn) {
		var item = locals[cdt][cdn];

		if (!item.item_code) {
			saashq.msgprint(__("Please select an item code before setting the warehouse."));
			saashq.model.set_value(cdt, cdn, "warehouse", "");
			return;
		}

		let item_args = {
			item_code: item.item_code,
			warehouse: item.warehouse,
			qty: item.consumed_quantity,
			serial_no: item.serial_no,
			company: frm.doc.company,
		};

		saashq.call({
			method: "erpnexus.stock.utils.get_incoming_rate",
			args: {
				args: item_args,
			},
			callback: function (r) {
				saashq.model.set_value(cdt, cdn, "valuation_rate", r.message);
			},
		});
	},

	consumed_quantity: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		saashq.model.set_value(cdt, cdn, "total_value", row.consumed_quantity * row.valuation_rate);
	},
});