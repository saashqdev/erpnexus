saashq.treeview_settings["Department"] = {
	ignore_fields: ["parent_department"],
	get_tree_nodes: "erpnexus.setup.doctype.department.department.get_children",
	add_tree_node: "erpnexus.setup.doctype.department.department.add_node",
	filters: [
		{
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			label: __("Company"),
		},
	],
	breadcrumb: "HR",
	root_label: "All Departments",
	get_tree_root: true,
	menu_items: [
		{
			label: __("New Department"),
			action: function () {
				saashq.new_doc("Department", true);
			},
			condition: 'saashq.boot.user.can_create.indexOf("Department") !== -1',
		},
	],
	onload: function (treeview) {
		treeview.make_tree();
	},
};
