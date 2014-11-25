import time

def dashboard():
    if not session.logged_in_user:
        session.redirection = URL('user', 'dashboard.html')
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

# The User Registration Page.
def new():
    # If we have come here externally, start process at the beginning.
    session.registration_stage = session.registration_stage or 0
    session.registration_stage = int(session.registration_stage)
    
    # Create the forms.
    form1 = SQLFORM.factory(db.user_address, db.user)
    form2 = SQLFORM.factory(db.user_address, db.user_credit_card)
    
    debug = open('bootable debugging.txt', 'a')
    debug.write(time.strftime("%H:%M.%S : "))
    debug.write("Stage = " + str(session.registration_stage) + "\n")
    debug.close()
    
    # If the second form has been submitted:
    if form2.validate(formname='billing-info') and session.registration_stage == 1:
        # Check if it's the same address.
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
        del session.registration_stage
        # If we were going somewhere:
        if session.redirection != None:
            # Then get back on track!
            target = session.redirection
            del session.redirection
            redirect(target)
        else:
            # Otherwise go to the homepage.
            redirect(URL('default', 'index.html'))
    
    # If the first form has been submitted:
    if form1.validate(formname='basic-info') and session.registration_stage == 0:
        # Capture the address in case the user will want the billing address to be the same.
        session.address_vars = db.user_address._filter_fields(form1.vars)
        # Check if an identical address exists in the database.
        id = None
        for address in db(db.user_address.id > 0).select():
            for key in address:
                if key != "id" and address[key] == session.address_vars[key]:
                    id = address.id
                    break
        # Capture the address ID after adding it to the database if necessary.
        if id != None:
            address_id = id
        else:
            address_id = db.user_address.insert(**db.user_address._filter_fields(form1.vars))
        # Captures the user variables, but do not add it to the database yet.
        session.user_vars = db.user._filter_fields(form1.vars)
        # Add the address ID to the user.
        session.user_vars["address_id"] = address_id
        # Go to the next stage.
        session.registration_stage = 1
        response.flash = 'Half way there...'
        
    debug = open('bootable debugging.txt', 'a')
    debug.write(time.strftime("%H:%M.%S : "))
    debug.write("Stage = " + str(session.registration_stage) + "\n\n")
    debug.close()
    
    # Return the varaibles to the view.
    forms = [form1, form2]
    stage = session.registration_stage
    return dict(form = forms[stage], stage = stage, formkey = forms[stage].formkey)

def profile():
    if not session.logged_in_user:
        session.redirection = URL('user', 'profile.html')
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

def login():
    # Create the form
    form = FORM(INPUT(_name='username', requires=[IS_NOT_EMPTY(), IS_IN_DB(db, "user.username")]), INPUT(_type='submit'))
    
    # If the form is valid
    if form.validate(formname="login") and db(db.user.username == form.vars.username).select():
        # Log the user in.
        session.logged_in_user = form.vars.username
        # Let them know they've been successful.
        session.flash = "You've successfully logged in!"
        # If we were going somewhere:
        if session.redirection != None:
            # Then get back on track!
            target = session.redirection
            del session.redirection
            redirect(target)
        else:
            # Otherwise go to the homepage.
            redirect(URL('default', 'index.html'))
    return dict(form=form)

def logout():
    if session.logged_in_user:
        del session.logged_in_user
        session.flash = "Logged out successfully."
    redirect(URL('default', 'index.html'))