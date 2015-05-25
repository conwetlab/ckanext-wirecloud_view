"use strict";

ckan.module('wirecloud_typeahead', function ($, _) {
	return {

		initialize: function () {

			$.proxyAll(this, /_on/);
			var endata = [];			
			var workspaces = {};
			var baseURL = this.options.baseurl;			

			$.each(this.options.workspaces, function (i, workspace) {				
				//We need to save the data as strings
				//in order to make the plugin work correctly
				endata.push(JSON.stringify(workspace));
			});

			this.el.on('click', function(){
				$(this).select();//This selects all text when the input is clicked				
			});

			this.el.typeahead({
				source: endata,
				matcher: function(item){
					//The matcher returns true searching by name and creator
					item = JSON.parse(item);
					var localName = item.name.toLowerCase();
					var creator = item.creator.toLowerCase();
					var localNameMatch = localName.indexOf(this.query.toLowerCase()) != -1;
					var creatorMatch = creator.indexOf(this.query.toLowerCase()) != -1

					return (localNameMatch || creatorMatch);
				},
				updater: function (item) {
					//The updater sets the input value to the correct URL				    
				    item = JSON.parse(item);									    
				    return baseURL + item.creator + "/" + item.name + "?mode=embedded";
				},
				highlighter: function(item) {
					//How the results are displayed
					item = JSON.parse(item);
					return "<b>" + item.name + "</b>  " + item.description;
				},
				sorter: function(items){
					//How the results are sorted
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