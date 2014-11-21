def dashboard():
    return dict()

def login():
    return dict()

# The User Registration Page.
def new():
    # If we have come here externally, start process at the beginning.
    if (request.vars.stage == None):
        request.vars.stage = 0
    else:
        request.vars.stage = int(request.vars.stage)
    
    # Create the forms such that they can be used across multiple instances of user/new
    form1 = SQLFORM.factory(db.user_address, db.user)
    form2 = SQLFORM.factory(db.user_address, db.user_credit_card)
    
    # If the first form has been submitted:
    if request.vars.stage == 0 and form1.validate(formname='basic-info'):
        # Capture the address in case the billing address is the same.
        session.address_vars = db.user_address._filter_fields(form1.vars)
        # Capture the address ID after adding it to the database.
        address_id = db.user_address.insert(**db.user_address._filter_fields(form1.vars))
        # Captures the user variables, but do not add it to the database yet.
        session.user_vars = db.user._filter_fields(form1.vars)
        # Add the address ID to the user.
        session.user_vars["address_id"] = address_id
        # Go to the next stage.
        request.vars.stage += 1
        response.flash = 'Half way there...'
    elif request.vars.stage == 0 and form1.errors:
        response.flash = 'form has errors'
    
    # If the second form has been submitted:
    if form2.validate(formname='billing-info'):
        session.second_form_validation = True
        # If they checked the previous address box.
        if form2.vars.previous_address:
            # Use the previous address (held in session vars).
            billing_address_id = session.user_vars["address_id"]
        else:
            # Otherwise, get the address values.
            billing_address_id = db.user_address.insert(**db.user_address._filter_fields(form2.vars))
        # Captures the credit card variables.
        credit_card_vars = db.user_credit_card._filter_fields(form2.vars)
        # Adds the billing address ID to the credit card.
        credit_card_vars["billing_address_id"] = billing_address_id
        # Add the credit card to the database, and get its ID.
        id = db.user_credit_card.insert(**credit_card_vars)
        # Add the credit card to the user stored in the session.
        session.user_vars["credit_card_id"] = id
        # Finally add the user to the database.
        db.user.insert(**session.user_vars)
        session.flash = "You've successfully logged in!"
        # If we were going somewhere:
        if session.redirection != None:
            # Then get back on track!
            redirect(session.redirection)
        else:
            # Otherwise go to the homepage.
            redirect(URL('default', 'index.html'))    
    elif request.vars.stage == 1 and form2.errors:
        response.flash = 'form has errors'
    
    # Return the varaibles to the view.
    return dict(forms = [form1, form2], stage = request.vars.stage)

def profile():
    return dict()