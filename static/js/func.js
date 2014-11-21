function toggle_billing_address(checkbox) {
    alert("toggled");
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
        if (document.getElementById("toggle_address_button").checked) {
//            document.getElementById("street_address").value = "{{ =session.address_vars['street_address']" }};
//            document.getElementById("city").value = "{{ =session.address_vars['city'] }}";
//            document.getElementById("postcode").value = "{{ =session.address_vars['postcode'] }}";
//            document.getElementById("country").value = "{{ =session.address_vars['country'] }}";
        } else {
            document.getElementById("postcode").value = document.getElementById("postcode1").value + 
                                                        document.getElementById("postcode2").value;
        }
    }
    return true;
}