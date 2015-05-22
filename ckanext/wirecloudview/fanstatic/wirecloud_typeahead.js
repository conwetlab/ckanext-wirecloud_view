"use strict";

ckan.module('wirecloud_typeahead', function ($, _) {
	return {
		initialize: function () {

			$.proxyAll(this, /_on/);

			workspaces = JSON.parse(this.options.workspaces);


			/* {  Workspaces JSON structure
			      "lastmodified":null,
			      "name":"webappWatchEnv",
			      "removable":false,
			      "creator":"tobias-goecke",
			      "active":false,
			      "shared":true,
			      "longdescription":"",
			      "id":3539,
			      "owned":false,
			      "description":""
			   }
			*/
			this.el.typeahead({
				source: function (query, process) {
					endata = [];
					map = {};

					$.each(data, function (i, workspace) {
						map[workspace.id] = workspace;
						endata.push(workspace.name);
					});

					process(endata);
				},
			});

		}
	};
});