"use strict";

ckan.module('wirecloud_option', function ($, _) {
	return {
		initialize: function () {

			$.proxyAll(this, /_on/);

			var elems = document.getElementsByClassName('option');

			for (var elem = 0; elem < elems.length; elem++){
				elems[elem].onclick = function () {

					if (this.classList.contains("small")) {
                        this.classList.remove("small");
					} else {
                        this.classList.add("small");
                    }
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
            };

            window.addEventListener("message", receiveMessage, false);
		}
	};
});
