function toggle_billing_address(checkbox) {
    var inputs = checkbox.parentElement.getElementsByTagName("input");
    var i;
    for (i = 0; i < inputs.length; i ++) {
        if (inputs[i] !== checkbox) {
            inputs[i].disabled = checkbox.checked;
        }
    }
}

function calculateHidden() {
//    <input name="postcode" class="string" id="no_table_postcode" type="text" value="">
//    <!-- Credit Card -->
//    <input name="expiry_date" class="date" id="no_table_expiry_date" type="text" value="" >
//    <input name="billing_address" class="string" id="no_table_billing_address" type="text" value="">
    document.getElementById("no_table_real_name").value = document.getElementById("forename").value + " " +
                                                          document.getElementById("surname").value;
    document.getElementById("no_table_birthdate").value = document.getElementById("dob_year").value + "-" +
                                                          document.getElementById("dob_month").value + "-" +
                                                          document.getElementById("dob_day").value;
    document.getElementById("no_table_postcode").value = document.getElementById("postcode1").value + 
                                                         document.getElementById("postcode2").value;
    if (document.getElementById("toggle_address_button").checked) {
        
//        <input name="street_address" class="string address-long" id="no_table_street_address" placeholder="Street Address" type="text" value="">
//        <br>
//        <input name="city" class="string address-short" id="no_table_city" placeholder="City" type="text" value="">
//        <br>
//        <input name="postcode1" class="string postcode-long" placeholder="Post" type="text" value="">
//        <input name="postcode2" class="string postcode-short" placeholder="Code" type="text" value="">
//        <br>
//        <input name="country" class="string address-short" id="no_table_country" placeholder="Country" type="text" value="">
        document.getElementById("")
        
    }
    return true;
}