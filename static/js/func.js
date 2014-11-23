function toggle_billing_address(checkbox) {
    var inputs = checkbox.parentElement.getElementsByTagName("input");
    var i;
    for (i = 0; i < inputs.length; i ++) {
        if (inputs[i] !== checkbox) {
            inputs[i].disabled = checkbox.checked;
        }
    }
}

function calculateHidden(stage) {
    if (stage == 0) {
        document.getElementById("real_name").value = document.getElementById("forename").value + " " +
                                                     document.getElementById("surname").value;
        document.getElementById("birthdate").value = document.getElementById("dob_year").value + "-" +
                                                     document.getElementById("dob_month").value + "-" +
                                                     document.getElementById("dob_day").value;
        document.getElementById("postcode").value = document.getElementById("postcode1").value + 
                                                    document.getElementById("postcode2").value;
    } else if (stage == 1) {
        document.getElementById("postcode").value = document.getElementById("postcode1").value + 
                                                    document.getElementById("postcode2").value;
    }
    return true;
}