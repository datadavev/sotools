// Functions for the thebe activate button and status field

function thebe_place_activate_button(){
  $('#thebelab-activate-button')
    .html('<input type="button"\
                  onclick="thebe_activate_button_function()"\
                  value="Activate"\
                  title="ThebeLab (requires internet):\nClick to activate code cells in this page.\nYou can then edit and run them.\nComputations courtesy of mybinder.org."\
                   class="thebe-status-field"/>');
}

function thebe_remove_activate_button(){
  $('#thebelab-activate-button').empty();
}

function thebe_place_status_field(){
  $('#thebelab-activate-button')
    .html('<span class="thebe-status-field"\
                title="ThebeLab status.\nClick `run` to execute code cells.\nComputations courtesy of mybinder.org.">Activating...\
          </span>');
}

function thebe_activate_cells() {
  thebelab.on("status", function (evt, data) {
    console.log("Status changed:", data.status, data.message);
    $("#thebelab-activate-button")
      .attr("class", "thebe-status-field thebe-status-" + data.status)
      .text(data.status);
    if (data.status == "ready") {
      var thebeInitCells = document.querySelectorAll('.thebelab-init');
      thebeInitCells.forEach((cell) => {
        console.log("Initializing ThebeLab with cell: " + cell.id);
        const initButton = cell.querySelector('.thebelab-run-button');
        initButton.click();
      });
    }
  });
}

