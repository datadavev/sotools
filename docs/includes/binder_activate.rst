.. include this to insert a Binder activation section.

How to run code on this page
----------------------------

.. thebe-button:: Activate Binder

All examples on this page can be run live in Mybinder_. To do so:

1. Click on the "Activate Binder" button
2. Wait for Binder to be active and the button turns green with the text "ready". This can take a while, you can watch
   progress in the browser's `javascript console`_. When a line like ``Kernel: connected (89dfd3c8...`` appears,
   Binder should be ready to go.

.. _Mybinder: https://mybinder.org/

.. raw:: html

    <script>
    $("#thebelab-activate-button").off("click");
    $("#thebelab-activate-button").click(function() {
        let activateButton = document.getElementById("thebelab-activate-button");
        if (activateButton.classList.contains('thebelab-active2')) {
            return;
        }
        thebe_place_status_field();
        thebe_activate_cells();
        activateButton.classList.add('thebelab-active2');
    });
    </script>

.. _javascript console: https://webmasters.stackexchange.com/questions/8525/how-do-i-open-the-javascript-console-in-different-browsers
