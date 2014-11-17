function toggle_billing_address(checkbox) {
    var inputs = checkbox.parentElement.getElementsByTagName("input");
    var i;
    for (i = 0; i < inputs.length; i ++) {
        if (inputs[i] !== checkbox) {
            inputs[i].disabled = !inputs[i].disabled;
        }
    }
}