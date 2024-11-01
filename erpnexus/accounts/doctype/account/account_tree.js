saashq.provide("saashq.treeview_settings");

saashq.treeview_settings["Account"] = {
	breadcrumb: "Accounts",
	title: __("Chart of Accounts"),
	get_tree_root: false,
	filters: [
		{
			fieldname: "company",
			fieldtype: "Select",
			options: erpnexus.utils.get_tree_options("company"),
			label: __("Company"),
			default: erpnexus.utils.get_tree_default("company"),
			on_change: function () {
				var me = saashq.treeview_settings["Account"].treeview;
				var company = me.page.fields_dict.company.get_value();
				if (!company) {
					saashq.throw(__("Please set a Company"));
				}
				saashq.call({
					method: "erpnexus.accounts.doctype.account.account.get_root_company",
					args: {
						company: company,
					},
					callback: function (r) {
						if (r.message) {
							let root_company = r.message.length ? r.message[0] : "";
							me.page.fields_dict.root_company.set_value(root_company);

							saashq.db.get_value(
								"Company",
								{ name: company },
								"allow_account_creation_against_child_company",
								(r) => {
									saashq.flags.ignore_root_company_validation =
										r.allow_account_creation_against_child_company;
								}
							);
						}
					},
				});
			},
		},
		{
			fieldname: "root_company",
			fieldtype: "Data",
			label: __("Root Company"),
			hidden: true,
			disable_onchange: true,
		},
	],
	root_label: "Accounts",
	get_tree_nodes: "erpnexus.accounts.utils.get_children",
	on_get_node: function (nodes, deep = false) {
		if (saashq.boot.user.can_read.indexOf("GL Entry") == -1) return;

		let accounts = [];
		if (deep) {
			// in case of `get_all_nodes`
			accounts = nodes.reduce((acc, node) => [...acc, ...node.data], []);
		} else {
			accounts = nodes;
		}

		saashq.db.get_single_value("Accounts Settings", "show_balance_in_coa").then((value) => {
			if (value) {
				const get_balances = saashq.call({
					method: "erpnexus.accounts.utils.get_account_balances",
					args: {
						accounts: accounts,
						company: cur_tree.args.company,
					},
				});

				get_balances.then((r) => {
					if (!r.message || r.message.length == 0) return;

					for (let account of r.message) {
						const node = cur_tree.nodes && cur_tree.nodes[account.value];
						if (!node || node.is_root) continue;

						// show Dr if positive since balance is calculated as debit - credit else show Cr
						const balance = account.balance_in_account_currency || account.balance;
						const dr_or_cr = balance > 0 ? __("Dr") : __("Cr");
						const format = (value, currency) => format_currency(Math.abs(value), currency);

						if (account.balance !== undefined) {
							node.parent && node.parent.find(".balance-area").remove();
							$(
								'<span class="balance-area pull-right">' +
									(account.balance_in_account_currency
										? format(
												account.balance_in_account_currency,
												account.account_currency
										  ) + " / "
										: "") +
									format(account.balance, account.company_currency) +
									" " +
									dr_or_cr +
									"</span>"
							).insertBefore(node.$ul);
						}
					}
				});
			}
		});
	},
	add_tree_node: "erpnexus.accounts.utils.add_ac",
	menu_items: [
		{
			label: __("New Company"),
			action: function () {
				saashq.new_doc("Company", true);
			},
			condition: 'saashq.boot.user.can_create.indexOf("Company") !== -1',
		},
	],
	fields: [
		{
			fieldtype: "Data",
			fieldname: "account_name",
			label: __("New Account Name"),
			reqd: true,
			description: __(
				"Name of new Account. Note: Please don't create accounts for Customers and Suppliers"
			),
		},
		{
			fieldtype: "Data",
			fieldname: "account_number",
			label: __("Account Number"),
			description: __("Number of new Account, it will be included in the account name as a prefix"),
		},
		{
			fieldtype: "Check",
			fieldname: "is_group",
			label: __("Is Group"),
			description: __(
				"Further accounts can be made under Groups, but entries can be made against non-Groups"
			),
		},
		{
			fieldtype: "Select",
			fieldname: "root_type",
			label: __("Root Type"),
			options: ["Asset", "Liability", "Equity", "Income", "Expense"].join("\n"),
			depends_on: "eval:doc.is_group && !doc.parent_account",
		},
		{
			fieldtype: "Select",
			fieldname: "account_type",
			label: __("Account Type"),
			options: saashq.get_meta("Account").fields.filter((d) => d.fieldname == "account_type")[0]
				.options,
			description: __("Optional. This setting will be used to filter in various transactions."),
		},
		{
			fieldtype: "Float",
			fieldname: "tax_rate",
			label: __("Tax Rate"),
			depends_on: 'eval:doc.is_group==0&&doc.account_type=="Tax"',
		},
		{
			fieldtype: "Link",
			fieldname: "account_currency",
			label: __("Currency"),
			options: "Currency",
			description: __("Optional. Sets company's default currency, if not specified."),
		},
	],
	ignore_fields: ["parent_account"],
	onload: function (treeview) {
		saashq.treeview_settings["Account"].treeview = {};
		$.extend(saashq.treeview_settings["Account"].treeview, treeview);
		function get_company() {
			return treeview.page.fields_dict.company.get_value();
		}

		// tools
		treeview.page.add_inner_button(
			__("Chart of Cost Centers"),
			function () {
				saashq.set_route("Tree", "Cost Center", { company: get_company() });
			},
			__("View")
		);

		treeview.page.add_inner_button(
			__("Opening Invoice Creation Tool"),
			function () {
				saashq.set_route("Form", "Opening Invoice Creation Tool", { company: get_company() });
			},
			__("View")
		);

		treeview.page.add_inner_button(
			__("Period Closing Voucher"),
			function () {
				saashq.set_route("List", "Period Closing Voucher", { company: get_company() });
			},
			__("View")
		);

		treeview.page.add_inner_button(
			__("Journal Entry"),
			function () {
				saashq.new_doc("Journal Entry", { company: get_company() });
			},
			__("Create")
		);
		treeview.page.add_inner_button(
			__("Company"),
			function () {
				saashq.new_doc("Company");
			},
			__("Create")
		);

		// financial statements
		for (let report of [
			"Trial Balance",
			"General Ledger",
			"Balance Sheet",
			"Profit and Loss Statement",
			"Cash Flow",
			"Accounts Payable",
			"Accounts Receivable",
		]) {
			treeview.page.add_inner_button(
				__(report),
				function () {
					saashq.set_route("query-report", report, { company: get_company() });
				},
				__("Financial Statements")
			);
		}
	},
	post_render: function (treeview) {
		saashq.treeview_settings["Account"].treeview["tree"] = treeview.tree;
		treeview.page.set_primary_action(
			__("New"),
			function () {
				let root_company = treeview.page.fields_dict.root_company.get_value();

				if (root_company) {
					saashq.throw(__("Please add the account to root level Company - {0}"), [root_company]);
				} else {
					treeview.new_node();
				}
			},
			"add"
		);
	},
	toolbar: [
		{
			label: __("Add Child"),
			condition: function (node) {
				return (
					saashq.boot.user.can_create.indexOf("Account") !== -1 &&
					(!saashq.treeview_settings[
						"Account"
					].treeview.page.fields_dict.root_company.get_value() ||
						saashq.flags.ignore_root_company_validation) &&
					node.expandable &&
					!node.hide_add
				);
			},
			click: function () {
				var me = saashq.views.trees["Account"];
				me.new_node();
			},
			btnClass: "hidden-xs",
		},
		{
			condition: function (node) {
				return !node.root && saashq.boot.user.can_read.indexOf("GL Entry") !== -1;
			},
			label: __("View Ledger"),
			click: function (node, btn) {
				saashq.route_options = {
					account: node.label,
					from_date: erpnexus.utils.get_fiscal_year(saashq.datetime.get_today(), true)[1],
					to_date: erpnexus.utils.get_fiscal_year(saashq.datetime.get_today(), true)[2],
					company:
						saashq.treeview_settings["Account"].treeview.page.fields_dict.company.get_value(),
				};
				saashq.set_route("query-report", "General Ledger");
			},
			btnClass: "hidden-xs",
		},
	],
	extend_toolbar: true,
};
