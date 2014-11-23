def dashboard():
    if not session.logged_in_user:
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

# The User Registration Page.
def new():
    # If we have come here externally, start process at the beginning.
    if (request.vars.stage == None):
        request.vars.stage = 0
    else:
        request.vars.stage = int(request.vars.stage)
    session.registration_stage = request.vars.stage
    
    # Create the forms such that they can be used across multiple instances of user/new
    form1 = SQLFORM.factory(db.user_address, db.user)
    form2 = SQLFORM.factory(db.user_address, db.user_credit_card)
    
    # If the second form has been submitted:
    if form2.validate(formname='billing-info'):
        # Check if it's the same address
        if session.address_vars == db.user_address._filter_fields(form2.vars):
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
        credit_card_id = db.user_credit_card.insert(**credit_card_vars)
        # Add the credit card to the user stored in the session.
        session.user_vars["credit_card_id"] = credit_card_id
        # Finally add the user to the database.
        user_id = db.user.insert(**session.user_vars)
        # Log in the user.
        session.logged_in_user = session.user_vars['username']
        session.flash = "You've successfully registered and have been logged in!"
        ## Remove session vars no longer needed.
        del session.user_vars
        del session.address_vars
        # If we were going somewhere:
        if session.redirection != None:
            # Then get back on track!
            redirect(session.redirection)
        else:
            # Otherwise go to the homepage.
            redirect(URL('default', 'index.html'))
    elif form2.errors:
        session.registration_stage = 1
        response.flash = 'form has errors'
    
    # If the first form has been submitted:
    if session.registration_stage == 0 and form1.validate(formname='basic-info'):
        # Capture the address in case the billing address is the same.
        session.address_vars = db.user_address._filter_fields(form1.vars)
        # Capture the address ID after adding it to the database.
        address_id = db.user_address.insert(**db.user_address._filter_fields(form1.vars))
        # Captures the user variables, but do not add it to the database yet.
        session.user_vars = db.user._filter_fields(form1.vars)
        # Add the address ID to the user.
        session.user_vars["address_id"] = address_id
        # Go to the next stage.
        session.registration_stage += 1
        response.flash = 'Half way there...'
    elif session.registration_stage == 0 and form1.errors:
        response.flash = 'form has errors'
    
    # Return the varaibles to the view.
    forms = [form1, form2]
    stage = session.registration_stage
    return dict(form = forms[stage], stage = stage, formkey = forms[stage].formkey)

def profile():
    if not session.logged_in_user:
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

def login():
    form = FORM(INPUT(_name='username', requires=[IS_NOT_EMPTY(), IS_IN_DB(db, "user.username")]),
               INPUT(_type='submit'))
    if form.validate(formname="login"):
        session.DEBUG = form.vars.username
        if db(db.user.username == form.vars.username).select():
            session.DEBUG = db(db.user.username == form.vars.username).select()
            session.logged_in_user = form.vars.username
            session.flash = "You've successfully logged in!"
            # If we were going somewhere:
            if session.redirection != None:
                # Then get back on track!
                redirect(session.redirection)
            else:
                # Otherwise go to the homepage.
                redirect(URL('default', 'index.html'))
    return dict(form=form)

def logout():
    del session.logged_in_user
    redirect(URL('default', 'index.html'))
    return dict()