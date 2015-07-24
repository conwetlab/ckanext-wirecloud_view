"use strict";

ckan.module('wirecloud_option', function ($, _) {
	return {
		initialize: function () {

			$.proxyAll(this, /_on/);
			var editor_url = this.options.editor;

			var elems = document.getElementsByClassName('option');

			for (var elem = 0; elem < elems.length; elem++){
				elems[elem].onclick = function(){

					if (this.className.indexOf("small") != -1){

						for(var elem2 = 0; elem2 < elems.length; elem2++){
							if (elems[elem2] != this){
								elems[elem2].className ="option small";
							}
						}
						this.className = "option";
					}
				}
			}
		}
	};
});