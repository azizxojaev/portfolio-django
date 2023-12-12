let wrapper = document.querySelector("#modal_wrapper");
let modal = document.querySelector("#modal");
let delete_link = document.querySelector("#delete_link");
let info_wrapper = document.querySelector("#info_wrapper");

let id = 0
function openModal(project_id) {
    wrapper.hidden = false
    modal.hidden = false
    id = project_id
}

function hideModal() {
    wrapper.hidden = true
    modal.hidden = true
}

function send_ajax() {
    $(`#project_${id}`).fadeOut("400", function() {
        $(this).remove();
        $.ajax({
            url: `delete_project/${id}`,
            method: "GET",
            dataType: "json",
        });
    });
    hideModal()
    $('#alert').removeClass('d-none').hide().fadeIn('400');
    setTimeout(function() {
        $('#alert').fadeOut('slow');
    }, 2000);
}
