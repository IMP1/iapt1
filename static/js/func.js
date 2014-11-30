/**
    Calculates hidden variables for user registration.
    Hidden variables are those the user shouldn't be entering themselves.
*/
function calculateHiddenRegistration(stage, form) {
    form = form.ownerDocument;
    if (stage == 0) {
        form.getElementById("birthdate").value = form.getElementById("dob_year").value + "-" +
                                                 form.getElementById("dob_month").value + "-" +
                                                 form.getElementById("dob_day").value;
        form.getElementById("postcode").value = form.getElementById("postcode1").value + 
                                                form.getElementById("postcode2").value;
    } else if (stage == 1) {
        form.getElementById("expiry_date").value = form.getElementById("expiry_date_year").value + "-" +
                                                   form.getElementById("expiry_date_month").value + "-" +
                                                   "01";
        form.getElementById("postcode").value = form.getElementById("postcode1").value + 
                                                form.getElementById("postcode2").value;
    }
    return true;
}

/**
    Calculates hidden variables for bootable creation.
    Hidden variables are those the user shouldn't be entering themselves.
*/
function calculateHiddenBootable(stage, form) {
    form = form.ownerDocument;
    if (stage == 0) {
        // Get the time and date now.
        creation_date = new Date();
        // Get into web2py format.
        creation_date = creation_date.getFullYear() + "-" + creation_date.getMonth() + "-" + creation_date.getDate() + " " + creation_date.toLocaleString().split(" ")[1];
        // Insert the values into the fields.
        form.getElementById("category_id").value = document.getElementById("category_name").selectedIndex + 1; // + 1 because database IDs start at 1
        form.getElementById("creation_date").value = creation_date;
    }
    return true;
}

function choosePledge(pledge_id) {
    document.getElementById("pledge_selection").value = pledge_id;
}
function deletePledge(pledge_id) {
    document.getElementById("pledge_deletion").value = pledge_id;
}
function editBootable(bootable_id) {
    document.getElementById("edit").value = bootable_id;
}
function publishBootable(bootable_id) {
    document.getElementById("publish").value = bootable_id;
}
function closeBootable(bootable_id) {
    document.getElementById("close").value = bootable_id;
}
function deleteBootable(bootable_id) {
    document.getElementById("bootable_deletion").value = bootable_id;
}

/**
    Updates the upload label to match the filename.
*/
function updateFileLabel(input) {
    document.getElementById("file-name").innerHTML = input.value;
}

/** 
    Used in bootable creation.
    Distinguished between adding another pledge, and finishing adding pledges.
    Setting the value of this field to 'finished' is interpreted by the controller
    as a sign that the user has pressed the Finish button and is finished.
*/
function finishUp() {
    // Set the value to finished (interpreted by the controller to move on).
    document.getElementById('finish').value = 'finished';
}

$('.alert').click(function() {
    $(".alert").hide();
});
$('.alert').attr('data-toggle', 'tooltip');
$('.alert').attr('title', 'Click to dismiss.');

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});
