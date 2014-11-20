def dashboard():
    return dict()

def login():
    return dict()

# The User Registration Page
def new():
    # If we have come here externally, start process at the beginning.
    if (request.vars.stage == None):
        request.vars.stage = 0
    else:
        request.vars.stage = int(request.vars.stage)
        
    # Create the forms
    form1 = SQLFORM.factory(db.user_address, db.user)
    form2 = SQLFORM.factory(db.user_address, db.user_credit_card)
    
    # If the first form has been submitted
    if form1.process().accepted:
        session.address_vars = db.user_address._filter_fields(form1.vars) ## DEBUGGING
        # Capture the address ID after adding it to the database.
        address_id = db.user_address.insert(**db.user_address._filter_fields(form1.vars))
        # Captures the user variables, but do not add it to the database yet.
        session.user_vars = db.user._filter_fields(form1.vars)
        # Add the address ID to the user
        session.user_vars["address_id"] = address_id
        # Go to the next stage
        request.vars.stage += 1
    elif form1.errors:
        response.flash = 'form has errors'
        
    if form2.process().accepted:
        billing_address_id = db.user_address.insert(**db.user_address._filter_fields(form2.vars))
        form2.vars.user_address = billing_address_id
        id = db.user_credit_card.insert(**db.user_credit_card._filter_fields(form2.vars))
        db.user.insert(**session.user_vars)
        
    return dict(forms = [form1, form2], stage = request.vars.stage)

def profile():
    return dict()