// Copyright (c) 2015, Saashq Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

saashq.provide("erpnexus.selling");

erpnexus.sales_common = {
	setup_selling_controller: function () {
		erpnexus.selling.SellingController = class SellingController extends erpnexus.TransactionController {
			setup() {
				super.setup();
				this.toggle_enable_for_stock_uom("allow_to_edit_stock_uom_qty_for_sales");
				this.frm.email_field = "contact_email";
			}

			onload() {
				super.onload();
				this.setup_queries();
				this.frm.set_query("shipping_rule", function (doc) {
					return {
						filters: {
							shipping_rule_type: "Selling",
							company: doc.company,
						},
					};
				});

				this.frm.set_query("project", function (doc) {
					return {
						query: "erpnexus.controllers.queries.get_project_name",
						filters: {
							customer: doc.customer,
							company: doc.company,
						},
					};
				});
			}

			setup_queries() {
				var me = this;

				$.each(
					[
						["customer", "customer"],
						["lead", "lead"],
					],
					function (i, opts) {
						if (me.frm.fields_dict[opts[0]]) me.frm.set_query(opts[0], erpnexus.queries[opts[1]]);
					}
				);

				me.frm.set_query("contact_person", erpnexus.queries.contact_query);
				me.frm.set_query("customer_address", erpnexus.queries.address_query);
				me.frm.set_query("shipping_address_name", erpnexus.queries.address_query);
				me.frm.set_query("dispatch_address_name", erpnexus.queries.dispatch_address_query);

				erpnexus.accounts.dimensions.setup_dimension_filters(me.frm, me.frm.doctype);

				if (this.frm.fields_dict.selling_price_list) {
					this.frm.set_query("selling_price_list", function () {
						return { filters: { selling: 1 } };
					});
				}

				if (this.frm.fields_dict.tc_name) {
					this.frm.set_query("tc_name", function () {
						return { filters: { selling: 1 } };
					});
				}

				if (!this.frm.fields_dict["items"]) {
					return;
				}

				if (this.frm.fields_dict["items"].grid.get_field("item_code")) {
					this.frm.set_query("item_code", "items", function () {
						return {
							query: "erpnexus.controllers.queries.item_query",
							filters: { is_sales_item: 1, customer: me.frm.doc.customer, has_variants: 0 },
						};
					});
				}

				if (
					this.frm.fields_dict["packed_items"] &&
					this.frm.fields_dict["packed_items"].grid.get_field("batch_no")
				) {
					this.frm.set_query("batch_no", "packed_items", function (doc, cdt, cdn) {
						return me.set_query_for_batch(doc, cdt, cdn);
					});
				}

				if (this.frm.fields_dict["items"].grid.get_field("item_code")) {
					this.frm.set_query("item_tax_template", "items", function (doc, cdt, cdn) {
						return me.set_query_for_item_tax_template(doc, cdt, cdn);
					});
				}
			}

			refresh() {
				super.refresh();

				saashq.dynamic_link = { doc: this.frm.doc, fieldname: "customer", doctype: "Customer" };

				this.frm.toggle_display(
					"customer_name",
					this.frm.doc.customer_name && this.frm.doc.customer_name !== this.frm.doc.customer
				);

				this.toggle_editable_price_list_rate();
			}

			customer() {
				var me = this;
				erpnexus.utils.get_party_details(this.frm, null, null, function () {
					me.apply_price_list();
				});
			}

			customer_address() {
				erpnexus.utils.get_address_display(this.frm, "customer_address");
				erpnexus.utils.set_taxes_from_address(
					this.frm,
					"customer_address",
					"customer_address",
					"shipping_address_name"
				);
			}

			shipping_address_name() {
				erpnexus.utils.get_address_display(this.frm, "shipping_address_name", "shipping_address");
				erpnexus.utils.set_taxes_from_address(
					this.frm,
					"shipping_address_name",
					"customer_address",
					"shipping_address_name"
				);
			}

			dispatch_address_name() {
				erpnexus.utils.get_address_display(this.frm, "dispatch_address_name", "dispatch_address");
			}

			sales_partner() {
				this.apply_pricing_rule();
			}

			campaign() {
				this.apply_pricing_rule();
			}

			selling_price_list() {
				this.apply_price_list();
				this.set_dynamic_labels();
			}

			discount_percentage(doc, cdt, cdn) {
				var item = saashq.get_doc(cdt, cdn);
				item.discount_amount = 0.0;
				this.apply_discount_on_item(doc, cdt, cdn, "discount_percentage");
			}

			discount_amount(doc, cdt, cdn) {
				if (doc.name === cdn) {
					return;
				}

				var item = saashq.get_doc(cdt, cdn);
				item.discount_percentage = 0.0;
				this.apply_discount_on_item(doc, cdt, cdn, "discount_amount");
			}

			commission_rate() {
				this.calculate_commission();
			}

			total_commission() {
				saashq.model.round_floats_in(this.frm.doc, [
					"amount_eligible_for_commission",
					"total_commission",
				]);

				const { amount_eligible_for_commission } = this.frm.doc;
				if (!amount_eligible_for_commission) return;

				this.frm.set_value(
					"commission_rate",
					flt((this.frm.doc.total_commission * 100.0) / amount_eligible_for_commission)
				);
			}

			allocated_percentage(doc, cdt, cdn) {
				var sales_person = saashq.get_doc(cdt, cdn);
				if (sales_person.allocated_percentage) {
					sales_person.allocated_percentage = flt(
						sales_person.allocated_percentage,
						precision("allocated_percentage", sales_person)
					);

					sales_person.allocated_amount = flt(
						(this.frm.doc.amount_eligible_for_commission * sales_person.allocated_percentage) /
							100.0,
						precision("allocated_amount", sales_person)
					);
					refresh_field(["allocated_amount"], sales_person);

					this.calculate_incentive(sales_person);
					refresh_field(
						["allocated_percentage", "allocated_amount", "commission_rate", "incentives"],
						sales_person.name,
						sales_person.parentfield
					);
				}
			}

			sales_person(doc, cdt, cdn) {
				var row = saashq.get_doc(cdt, cdn);
				this.calculate_incentive(row);
				refresh_field("incentives", row.name, row.parentfield);
			}

			warehouse(doc, cdt, cdn) {
				if (doc.docstatus === 0 && doc.is_return && !doc.return_against) {
					saashq.model.set_value(cdt, cdn, "incoming_rate", 0.0);
				}

				this.set_actual_qty(doc, cdt, cdn);
			}

			set_actual_qty(doc, cdt, cdn) {
				let row = locals[cdt][cdn];
				let sales_doctypes = ["Sales Invoice", "Delivery Note", "Sales Order"];

				if (row.item_code && row.warehouse && sales_doctypes.includes(doc.doctype)) {
					saashq.call({
						method: "erpnexus.stock.get_item_details.get_bin_details",
						args: {
							item_code: row.item_code,
							warehouse: row.warehouse,
						},
						callback(r) {
							if (r.message) {
								saashq.model.set_value(cdt, cdn, "actual_qty", r.message.actual_qty);
							}
						},
					});
				}
			}

			toggle_editable_price_list_rate() {
				var df = saashq.meta.get_docfield(
					this.frm.doc.doctype + " Item",
					"price_list_rate",
					this.frm.doc.name
				);
				var editable_price_list_rate = cint(saashq.defaults.get_default("editable_price_list_rate"));

				if (df && editable_price_list_rate) {
					const parent_field = saashq.meta.get_parentfield(
						this.frm.doc.doctype,
						this.frm.doc.doctype + " Item"
					);
					if (!this.frm.fields_dict[parent_field]) return;

					this.frm.fields_dict[parent_field].grid.update_docfield_property(
						"price_list_rate",
						"read_only",
						0
					);
				}
			}

			calculate_commission() {
				if (!this.frm.fields_dict.commission_rate || this.frm.doc.docstatus === 1) return;

				if (this.frm.doc.commission_rate > 100) {
					this.frm.set_value("commission_rate", 100);
					saashq.throw(
						`${__(
							saashq.meta.get_label(this.frm.doc.doctype, "commission_rate", this.frm.doc.name)
						)} ${__("cannot be greater than 100")}`
					);
				}

				this.frm.doc.amount_eligible_for_commission = this.frm.doc.items.reduce(
					(sum, item) => (item.grant_commission ? sum + item.base_net_amount : sum),
					0
				);

				this.frm.doc.total_commission = flt(
					(this.frm.doc.amount_eligible_for_commission * this.frm.doc.commission_rate) / 100.0,
					precision("total_commission")
				);

				refresh_field(["amount_eligible_for_commission", "total_commission"]);
			}

			calculate_contribution() {
				var me = this;
				$.each(this.frm.doc.doctype.sales_team || [], function (i, sales_person) {
					saashq.model.round_floats_in(sales_person);
					if (!sales_person.allocated_percentage) return;

					sales_person.allocated_amount = flt(
						(me.frm.doc.amount_eligible_for_commission * sales_person.allocated_percentage) /
							100.0,
						precision("allocated_amount", sales_person)
					);
				});
			}

			calculate_incentive(row) {
				if (row.allocated_amount) {
					row.incentives = flt(
						(row.allocated_amount * row.commission_rate) / 100.0,
						precision("incentives", row)
					);
				}
			}

			set_dynamic_labels() {
				super.set_dynamic_labels();
				this.set_product_bundle_help(this.frm.doc);
			}

			set_product_bundle_help(doc) {
				if (!this.frm.fields_dict.packing_list) return;
				if ((doc.packed_items || []).length) {
					$(this.frm.fields_dict.packing_list.row.wrapper).toggle(true);

					if (["Delivery Note", "Sales Invoice"].includes(doc.doctype)) {
						var help_msg =
							"<div class='alert alert-warning'>" +
							__(
								"For 'Product Bundle' items, Warehouse, Serial No and Batch No will be considered from the 'Packing List' table. If Warehouse and Batch No are same for all packing items for any 'Product Bundle' item, those values can be entered in the main Item table, values will be copied to 'Packing List' table."
							) +
							"</div>";
						saashq.meta.get_docfield(doc.doctype, "product_bundle_help", doc.name).options =
							help_msg;
					}
				} else {
					$(this.frm.fields_dict.packing_list.row.wrapper).toggle(false);
					if (["Delivery Note", "Sales Invoice"].includes(doc.doctype)) {
						saashq.meta.get_docfield(doc.doctype, "product_bundle_help", doc.name).options = "";
					}
				}
				refresh_field("product_bundle_help");
			}

			company_address() {
				var me = this;
				if (this.frm.doc.company_address) {
					saashq.call({
						method: "saashq.contacts.doctype.address.address.get_address_display",
						args: { address_dict: this.frm.doc.company_address },
						callback: function (r) {
							if (r.message) {
								me.frm.set_value("company_address_display", r.message);
							}
						},
					});
				} else {
					this.frm.set_value("company_address_display", "");
				}
			}

			conversion_factor(doc, cdt, cdn, dont_fetch_price_list_rate) {
				super.conversion_factor(doc, cdt, cdn, dont_fetch_price_list_rate);
			}

			qty(doc, cdt, cdn) {
				super.qty(doc, cdt, cdn);
			}

			pick_serial_and_batch(doc, cdt, cdn) {
				let item = locals[cdt][cdn];
				let me = this;

				saashq.db.get_value("Item", item.item_code, ["has_batch_no", "has_serial_no"]).then((r) => {
					if (r.message && (r.message.has_batch_no || r.message.has_serial_no)) {
						item.has_serial_no = r.message.has_serial_no;
						item.has_batch_no = r.message.has_batch_no;
						item.type_of_transaction = item.qty > 0 ? "Outward" : "Inward";

						item.title = item.has_serial_no ? __("Select Serial No") : __("Select Batch No");

						if (item.has_serial_no && item.has_batch_no) {
							item.title = __("Select Serial and Batch");
						}

						new erpnexus.SerialBatchPackageSelector(me.frm, item, (r) => {
							if (r) {
								let qty = Math.abs(r.total_qty);
								if (doc.is_return) {
									qty = qty * -1;
								}

								saashq.model.set_value(item.doctype, item.name, {
									serial_and_batch_bundle: r.name,
									use_serial_batch_fields: 0,
									incoming_rate: r.avg_rate,
									qty:
										qty /
										flt(
											item.conversion_factor || 1,
											precision("conversion_factor", item)
										),
								});
							}
						});
					}
				});
			}

			update_auto_repeat_reference(doc) {
				if (doc.auto_repeat) {
					saashq.call({
						method: "saashq.automation.doctype.auto_repeat.auto_repeat.update_reference",
						args: {
							docname: doc.auto_repeat,
							reference: doc.name,
						},
						callback: function (r) {
							if (r.message == "success") {
								saashq.show_alert({
									message: __("Auto repeat document updated"),
									indicator: "green",
								});
							} else {
								saashq.show_alert({
									message: __("An error occurred during the update process"),
									indicator: "red",
								});
							}
						},
					});
				}
			}

			project() {
				let me = this;
				if (["Delivery Note", "Sales Invoice", "Sales Order"].includes(this.frm.doc.doctype)) {
					if (this.frm.doc.project) {
						saashq.call({
							method: "erpnexus.projects.doctype.project.project.get_cost_center_name",
							args: { project: this.frm.doc.project },
							callback: function (r, rt) {
								if (!r.exc) {
									$.each(me.frm.doc["items"] || [], function (i, row) {
										if (r.message) {
											saashq.model.set_value(
												row.doctype,
												row.name,
												"cost_center",
												r.message
											);
											saashq.msgprint(
												__(
													"Cost Center For Item with Item Code {0} has been Changed to {1}",
													[row.item_name, r.message]
												)
											);
										}
									});
								}
							},
						});
					}
				}
			}

			coupon_code() {
				this.frm.set_value("discount_amount", 0);
				this.frm.set_value("additional_discount_percentage", 0);
			}
		};
	},
};

erpnexus.pre_sales = {
	set_as_lost: function (doctype) {
		saashq.ui.form.on(doctype, {
			set_as_lost_dialog: function (frm) {
				var dialog = new saashq.ui.Dialog({
					title: __("Set as Lost"),
					fields: [
						{
							fieldtype: "Table MultiSelect",
							label: __("Lost Reasons"),
							fieldname: "lost_reason",
							options:
								frm.doctype === "Opportunity"
									? "Opportunity Lost Reason Detail"
									: "Quotation Lost Reason Detail",
							reqd: 1,
						},
						{
							fieldtype: "Table MultiSelect",
							label: __("Competitors"),
							fieldname: "competitors",
							options: "Competitor Detail",
						},
						{
							fieldtype: "Small Text",
							label: __("Detailed Reason"),
							fieldname: "detailed_reason",
						},
					],
					primary_action: function () {
						let values = dialog.get_values();

						frm.call({
							doc: frm.doc,
							method: "declare_enquiry_lost",
							args: {
								lost_reasons_list: values.lost_reason,
								competitors: values.competitors ? values.competitors : [],
								detailed_reason: values.detailed_reason,
							},
							callback: function (r) {
								dialog.hide();
								frm.reload_doc();
							},
						});
					},
					primary_action_label: __("Declare Lost"),
				});

				dialog.show();
			},
		});
	},
};
