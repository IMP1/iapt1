import time

def dashboard():
    if not session.logged_in_user:
        session.redirection = URL('user', 'dashboard.html')
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
        
    if request.vars.edit:
        # Redirect to the edit page for this bootable.
        redirect(URL('bootable', 'edit.html', vars={'bootable_id': request.vars.edit}))
    elif request.vars.publish:
        # Edit the status of the variable.
        record = db.bootable(request.vars.publish)
        updates = {'status_id': 2}
        record.update_record(**db.bootable._filter_fields(updates))
    elif request.vars.close:
        # Edit the status of the variable.
        record = db.bootable(request.vars.close)
        pledges = db((db.bootable_pledges_made.pledge_id == db.bootable_pledges.id) & (db.bootable_pledges.bootable_id == record.id)).select()
        # Get the total amount funded.
        total = 0
        for p in pledges:
            total += p.cost
        # If it's unsuccessful:
        if total < record.funding_goal:
            # Set the status to Not Funded.
            updates = {'status_id': 4}
        else:
            # Else, set the status to Funded.
            updates = {'status_id': 3}
        # Update the database.
        record.update_record(**db.bootable._filter_fields(updates))
    elif request.vars.bootable_deletion:
        response.flash = "'" + str(db.bootable(request.vars.bootable_deletion).title) + "' deleted."
        # Delete the bootable.
        db(db.bootable.id == int(request.vars.bootable_deletion)).delete()
    
    return dict()

# The User Registration Page.
def new():
    # If we have come here externally, start process at the beginning.
    request.vars.registration_stage = request.vars.registration_stage or 0
    request.vars.registration_stage = int(request.vars.registration_stage)
    
    # Create the forms.
    form1 = SQLFORM.factory(db.user_address, db.user)
    form2 = SQLFORM.factory(db.user_address, db.user_credit_card)
    
    # If the second form has been submitted:
    if form2.validate(formname='billing-info') and request.vars.registration_stage == 1:
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
        # Check if an identical credit card exists in the databas.
        id = None
        for credit_card in db(db.user_credit_card.id > 0).select():
            for key in credit_card:
                if key != "id" and key in credit_card_vars and credit_card[key] == credit_card_vars[key]:
                    id = credit_card.id
                    break
        # Add the credit card to the database, and get its ID.
        if id != None:
            credit_card_id = id
        else:
            credit_card_id = db.user_credit_card.insert(**credit_card_vars)
        # Add the credit card to the user stored in the session.
        session.user_vars["credit_card_id"] = credit_card_id
        # Finally add the user to the database.
        user_id = db.user.insert(**session.user_vars)
        # Log in the user.
        session.logged_in_user = user_id
        session.flash = "You've successfully registered and have been logged in!"
        ## Remove session vars no longer needed.
        del session.user_vars
        del session.address_vars
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
    if form1.validate(formname='basic-info') and request.vars.registration_stage == 0:
        # Capture the address in case the user will want the billing address to be the same.
        session.address_vars = db.user_address._filter_fields(form1.vars)
        # Check if an identical address exists in the database.
        id = None
        for address in db(db.user_address.id > 0).select():
            for key in address:
                if key != "id" and key in session.address_vars and address[key] == session.address_vars[key]:
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
        request.vars.registration_stage = 1
        response.flash = 'Half way there...'
    
    # Return the varaibles to the view.
    forms = [form1, form2]
    stage = request.vars.registration_stage
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
        user = db(db.user.username == form.vars.username).select(db.user.id)[0]
        session.logged_in_user = user.id
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