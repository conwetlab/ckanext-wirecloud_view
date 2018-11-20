"use strict";

ckan.module('wirecloud_option', function ($, _) {
	return {
		initialize: function () {

			$.proxyAll(this, /_on/);

			var elems = document.getElementsByClassName('option');

			for (var elem = 0; elem < elems.length; elem++){
				elems[elem].onclick = function () {
                    $("graph_editor_div").toggle("fast");
				}
			}

            var receiveMessage = function receiveMessage(event) {
                // For Chrome, the origin property is in the event.originalEvent object.
                // var origin = event.origin || event.originalEvent.origin;
                // if (origin !== "http://example.org:8080") {
                //    return;
                //}

                document.getElementById("field-dashboard").value = event.data;
			    document.getElementsByClassName('option')[0].classList.add("small");
                // Assure hidden at start
                $("graph_editor_div").toggle(false);
            };

            window.addEventListener("message", receiveMessage, false);
		}
	};
});
