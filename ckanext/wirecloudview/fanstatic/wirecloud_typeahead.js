"use strict";

ckan.module('wirecloud_typeahead', function ($, _) {
	return {
		initialize: function () {

			$.proxyAll(this, /_on/);
			var endata = [];			
			var workspaces = {};
			var baseURL = this.options.baseurl;			

			$.each(this.options.workspaces, function (i, workspace) {
				//workspaces[workspace.id] = workspace;
				endata.push(JSON.stringify(workspace));
			});

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
				source: endata,
				matcher: function(item){
					item = JSON.parse(item);
					var localName = item.name.toLowerCase();
					var creator = item.creator.toLowerCase();
					var localNameMatch = localName.indexOf(this.query.toLowerCase()) != -1;
					var creatorMatch = creator.indexOf(this.query.toLowerCase()) != -1

					return (localNameMatch || creatorMatch);
				},
				updater: function (item) {
				    //TODO Associate the id with the item and save the real item
				    item = JSON.parse(item);									    
				    return baseURL + item.creator + "/" + item.name ;
				},
				highlighter: function(item) {
					item = JSON.parse(item);
					return item.name;
				},
				sorter: function(items){
					var beginswith = []
					, caseSensitive = []
					, caseInsensitive = []
					, item

					while (item = items.shift()) {
						var name = JSON.parse(item).name;
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