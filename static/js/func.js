function toggle_billing_address(checkbox) {
    var inputs = checkbox.parentElement.getElementsByTagName("input");
    var i;
    for (i = 0; i < inputs.length; i ++) {
        if (inputs[i] !== checkbox) {
            inputs[i].disabled = checkbox.checked;
        }
    }
}

function calculateHiddenRegistration(stage, form) {
    form = form.ownerDocument
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

function calculateHiddenBootable(stage, form) {
    form = form.ownerDocument
    if (stage == 0) {
        form.getElementById("category_id").value = document.getElementById("category_name").selectedIndex;
    }
    return true;
}

function updateFileLabel(input) {
    document.getElementById("file-name").innerHTML = input.value;
}

$('.alert').click(function() {
    $(".alert").hide();
});
$('.alert').attr('data-toggle', 'tooltip');
$('.alert').attr('title', 'Click to dismiss.');

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});