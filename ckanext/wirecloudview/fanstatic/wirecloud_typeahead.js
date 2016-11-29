"use strict";

ckan.module('wirecloud_typeahead', function ($, _) {

    var toString = function toString() {
        return this.owner + '/' + this.name;
    };

	return {

		initialize: function () {

			$.proxyAll(this, /_on/);
			var workspaces = this.options.workspaces;

            // Add a toString method to workspaces
            this.options.workspaces.forEach(function (workspace) {
                workspace.toString = toString;
            });

            // Select input text on focus
			this.el.on('focus', function () {
				$(this).select();
			});

			this.el.typeahead({
				source: workspaces,
				matcher: function (item) {
					var localName = item.name.toLowerCase();
					var owner = item.owner.toLowerCase();
					var localNameMatch = localName.indexOf(this.query.toLowerCase()) != -1;
					var ownerMatch = owner.indexOf(this.query.toLowerCase()) != -1

					return (localNameMatch || ownerMatch);
				},
				updater: function (dashboard) {
				    return dashboard;
				},
				highlighter: function(item) {
					return "<b>" + item.owner + "/" + item.name + "</b>  " + item.description;
				},
				sorter: function (items) {
					var beginswith = [],
					    caseSensitive = [],
					    caseInsensitive = [],
					    item;

					while (item = items.shift()) {
						var name = item.name;
						if (!name.toLowerCase().indexOf(this.query.toLowerCase())) beginswith.push(item)
						else if (~name.indexOf(this.query)) caseSensitive.push(item)
						else caseInsensitive.push(item)
					}

					return beginswith.concat(caseSensitive, caseInsensitive)
				}
			});

		}
	};
});
