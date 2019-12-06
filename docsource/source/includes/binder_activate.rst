.. include this to insert a Binder activation section.

Running code on this page
-------------------------

All examples on this page can be run live in Binder. To do so:

1. Click on the "Activate Binder" button
2. Wait for Binder to be active. This can take a while, you can watch progress in your
   browser's `javascript console`_. When a line like ``Kernel: connected (89dfd3c8...`` appears,
   Binder should be ready to go.
3. Run the following **before** any other script on the page. This sets the right
   path context for loading examples etc.

.. thebe-button:: Activate Binder

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


.. jupyter-execute::
   :hide-code:
   :hide-output:

   import os
   try:
       os.chdir("docsource/source")
   except:
       pass
   print("Page is ready. You can now run other code blocks on this page.")

.. _javascript console: https://webmasters.stackexchange.com/questions/8525/how-do-i-open-the-javascript-console-in-different-browsers
