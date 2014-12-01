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
        billing_address_id = db.user_address.insert(**db.user_address._filter_fields(form2.vars))
        # Captures the credit card variables.
        credit_card_vars = db.user_credit_card._filter_fields(form2.vars)
        # Adds the billing address ID to the credit card.
        credit_card_vars["billing_address_id"] = billing_address_id
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
        
    form1 = SQLFORM(db.user, db.user(session.logged_in_user))
    form2 = SQLFORM(db.user_address)
    form3 = SQLFORM(db.user_credit_card)
    form4 = SQLFORM(db.user_address)
    
    if form1.validate(formname="info"):
        response.flash = "User information updated!"
        # Update basic information.
        user = db.user(session.logged_in_user)
        user.update_record(**db.user._filter_fields(form1.vars))
    
    if form2.validate(formname="address"):
        response.flash = "Address updated!"
        # Update address.
        user = db.user(session.logged_in_user)
        address = db.user_address(user.address_id)
        address.update_record(**db.user_address._filter_fields(form2.vars))
    
    if form3.validate(formname="payment"):
        response.flash = "Credit card information updated!"
        # Update credit card information.
        user = db.user(session.logged_in_user)
        credit_card = db.user_credit_card(user.credit_card_id)
        credit_card.update_record(**db.user_credit_card._filter_fields(form3.vars))
    
    if form4.validate(formname="billing_address"):
        response.flash = "Billing address updated!"
        # Update billing address.
        user = db.user(session.logged_in_user)
        credit_card = db.user_credit_card(user.credit_card_id)
        address = db.user_address(credit_card.billing_address_id)
        address.update_record(**db.user_address._filter_fields(form4.vars))
    
    return dict(form1 = form1, form2 = form2, form3 = form3, form4 = form4, formkey1 = form1.formkey, formkey2 = form2.formkey, formkey3 = form3.formkey, formkey4 = form4.formkey)

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