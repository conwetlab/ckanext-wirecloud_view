"use strict";

ckan.module('wirecloud_option', function ($, _) {
    return {
        initialize: function () {

            $.proxyAll(this, /_on/);

            var elems = document.getElementsByClassName('option');

            for (var elem = 0; elem < elems.length; elem++){
                elems[elem].onclick = function () {
                    $("#graph_editor_div").toggle("fast");
                }
            }
            // Assure hidden at start
            $("#graph_editor_div").toggle(false);

            var receiveMessage = function receiveMessage(event) {
                // Avoid multiple events coming from within CKAN server
                var u = new URL(document.getElementById("graph_editor").src);
                if (event.origin.startsWith(u.protocol + "//" + u.host)) {
                    document.getElementById("field-dashboard").value = event.data;
                    // Hide after creating dashboard
                    $("#graph_editor_div").toggle(false);
                }
            };

            window.addEventListener("message", receiveMessage, false);
        }
    };
});
