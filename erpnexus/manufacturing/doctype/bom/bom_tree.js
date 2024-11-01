saashq.treeview_settings["BOM"] = {
	get_tree_nodes: "erpnexus.manufacturing.doctype.bom.bom.get_children",
	filters: [
		{
			fieldname: "bom",
			fieldtype: "Link",
			options: "BOM",
			label: __("BOM"),
		},
	],
	title: "BOM",
	breadcrumb: "Manufacturing",
	disable_add_node: true,
	root_label: "BOM", //fieldname from filters
	get_tree_root: false,
	show_expand_all: false,
	get_label: function (node) {
		if (node.data.qty) {
			return node.data.qty + " x " + node.data.item_code;
		} else {
			return node.data.item_code || node.data.value;
		}
	},
	onload: function (me) {
		var label = saashq.get_route()[0] + "/" + saashq.get_route()[1];
		if (saashq.pages[label]) {
			delete saashq.pages[label];
		}

		var filter = me.opts.filters[0];
		if (saashq.route_options && saashq.route_options[filter.fieldname]) {
			var val = saashq.route_options[filter.fieldname];
			delete saashq.route_options[filter.fieldname];
			filter.default = "";
			me.args[filter.fieldname] = val;
			me.root_label = val;
			me.page.set_title(val);
		}
		me.make_tree();
	},
	toolbar: [
		{ toggle_btn: true },
		{
			label: __("Edit"),
			condition: function (node) {
				return node.expandable;
			},
			click: function (node) {
				saashq.set_route("Form", "BOM", node.data.value);
			},
		},
	],
	menu_items: [
		{
			label: __("New BOM"),
			action: function () {
				saashq.new_doc("BOM", true);
			},
			condition: 'saashq.boot.user.can_create.indexOf("BOM") !== -1',
		},
	],
	onrender: function (node) {
		if (node.is_root && node.data.value != "BOM") {
			saashq.model.with_doc("BOM", node.data.value, function () {
				var bom = saashq.model.get_doc("BOM", node.data.value);
				node.data.image = escape(bom.image) || "";
				node.data.description = bom.description || "";
				node.data.item_code = bom.item || "";
			});
		}
	},
	view_template: "bom_item_preview",
};
