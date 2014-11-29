## BOOTABLE SEARCH PAGE
def search():
    session.clear()
    search_vars = request.vars
    return dict(search_vars = search_vars)

## BOOTABLE CREATION PAGE
def create():
    if not session.logged_in_user:
        session.redirection = URL('bootable', 'create.html')
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    # If we have come here externally, start process at the beginning.
    request.vars.creation_stage = request.vars.creation_stage or 0
    request.vars.creation_stage = int(request.vars.creation_stage)
    
    # Create the forms
    form1 = SQLFORM.factory(db.bootable)
    form2 = SQLFORM.factory(db.bootable.description, db.bootable.author)
    form3 = SQLFORM.factory(db.bootable_pledges)
    
    # If we're deleting we don't need the form to be filled out, but it needs to pass validation for a formkey to be created.
    placeholders = {}
    # If a delete pledge button has been pressed:
    if request.vars.pledge_deletion and request.vars.creation_stage == 2:
        # Delete the pledge:
        db(db.bootable_pledges.id == int(request.vars.pledge_deletion)).delete()
        # If we used placeholder field values to placate web2py's form validation (we don't need it to delete pledges):
        placeholders['title'] = request.vars['title']
        request.vars['title'] = "Placeholder Title"
        placeholders['cost'] = request.vars['cost']
        request.vars['cost'] = 0
    
    # If the third form has been submitted:
    if form3.validate(formname='pledges') and request.vars.creation_stage == 2:
        if request.vars.pledge_deletion:
            response.flash = "Pledge deleted."
        else:
            # If the button pressed was the finish button:
            if request.vars.finish:
                session.flash = "You've successfully created a bootable. Edit to your heart's content and then publish it when it's ready!"
                # If we were going somewhere:
                if session.redirection != None:
                    # Then get back on track!
                    target = session.redirection
                    del session.redirection
                    redirect(target)
                else:
                    # Otherwise go to the homepage.
                    target = session.bootable_id
                    del session.bootable_id
                    redirect(URL('bootable', 'edit.html', vars={'bootable_id': target}))
            else:
                response.flash = "Pledge added!"
                # Add the pledge.
                db.bootable_pledges.insert(**db.bootable_pledges._filter_fields(form3.vars))
                # Don't go anywhere because more pledges can be added.
    # If we've clicked on finish, we don't need the form to be filled out (only if there is at least one available pledge):
    elif request.vars.finish and db(db.bootable_pledges.bootable_id == session.bootable_id).select() and request.vars.creation_stage == 2:
        session.flash = "You've successfully created a bootable. Edit to your heart's content and then publish it when it's ready!"
        # If we were going somewhere:
        if session.redirection != None:
            # Then get back on track!
            target = session.redirection
            del session.redirection
            redirect(target)
        else:
            # Otherwise go to the homepage.
            target = session.bootable_id
            del session.bootable_id
            redirect(URL('bootable', 'edit.html', vars = dict(bootable=target)))
        
    # If the second form has been submitted:
    if form2.validate(formname='description') and request.vars.creation_stage == 1:        
        # Update the bootable with the description and about information
        record = db.bootable(session.bootable_id)
        form2.vars.about = request.vars.about
        record.update_record(**db.bootable._filter_fields(form2.vars))
        # Go to the next stage.
        request.vars.creation_stage = 2
        response.flash = "Nearly done!"
    
    # If the first form has been submitted:
    if form1.validate(formname='basic-info') and request.vars.creation_stage == 0:
        # Add the bootable to the database and capture its id.
        session.bootable_id = db.bootable.insert(**db.bootable._filter_fields(form1.vars))
        # Go to the next stage.
        request.vars.creation_stage = 1
        response.flash = "Not much more to do!"
    
    # If we've used placeholders, put them back.
    for key in placeholders:
        request.vars[key] = placeholders[key]
    
    forms = [form1, form2, form3]
    stage = request.vars.creation_stage
    return dict(form = forms[stage], stage = stage, formkey = forms[stage].formkey)

## BOOTABLE EDIT PAGE
def edit():
    if not session.logged_in_user:
        session.redirection = URL('bootable', 'edit.html')
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    if db.bootable(request.vars.bootable_id).author != session.logged_in_user:
        redirect(URL('bootable', 'view.html', vars={'bootable_id': request.vars.bootable_id}))
        
    form1 = SQLFORM.factory(db.bootable)
    form2 = SQLFORM.factory(db.bootable_pledges)
    
    # If we're deleting we don't need the form to be filled out, but it needs to pass validation for a formkey to be created.
    placeholders = {}
    # If we're deleting a pledge:
    if request.vars.pledge_deletion:
        # Delete the pledge.
        db(db.bootable_pledges.id == int(request.vars.pledge_deletion)).delete()
        # If we used placeholder field values to placate web2py's form validation (we don't need it to delete pledges).
        placeholders['title'] = request.vars['title']
        request.vars['title'] = "Placeholder Title"
        placeholders['cost'] = request.vars['cost']
        request.vars['cost'] = 0
    
    # If we are adding a pledge:
    if form2.validate(formname="pledge"):
        if request.vars.pledge_deletion:
            response.flash = "Pledge deleted!"
        else:
            response.flash = "Pledge added!"
            # Add the id to the pledge.
            form2.vars.bootable_id = request.vars.bootable_id
            # Add the new pledge to the database.
            db.bootable_pledges.insert(**db.bootable_pledges._filter_fields(form2.vars))
    
    # If one of the bootable buttons was pressed:
    if form1.validate(formname="bootable"):
        # If the delete button was pressed.
        if request.vars.bootable_deletion:
            session.flash = "'" + str(db.bootable(request.vars.bootable_deletion).title) + "' deleted."
            # Delete the bootable.
            db(db.bootable.id == int(request.vars.bootable_id)).delete()
            # Redirect as there's nothing left here now.
            redirect(URL('user', 'dashboard.html'))
        # Otherwise, we need to update.
        else:
            response.flash = "Bootable updated!"
            # Update the bootable.
            record = db.bootable(request.vars.bootable_id)
            # Since files can't be set up to be automatically selected in the input,
            # If the file is empty (hasn't been changed):
            if not form1.vars['image']:
                # Change it to what it is currently in the database.
                form1.vars['image'] = record.image
            record.update_record(**db.bootable._filter_fields(form1.vars))
            # If we're updating and publishing:
            if request.vars.publish:
                # Publish
                record = db.bootable(request.vars.publish)
                updates = {'status_id': 2}
                record.update_record(**db.bootable._filter_fields(updates))
                # Redirect to the the dashboard as it's no longer editable.
                redirect(URL('user', 'dashboard.html'))
        
    # If we've used placeholders, put them back.
    for key in placeholders:
        request.vars[key] = placeholders[key]
        
    return dict(form1 = form1, form2 = form2, formkey1 = form1.formkey, formkey2 = form2.formkey)

## BOOTABLE PAGE VIEW
def view():
    # If this bootable isn't available for pledging:
    if db.bootable(request.vars.bootable_id).status_id != 2:
        # redirect to the homepage.
        redirect(URL('default', 'index.html'))
    return dict()

## BOOTABLE PLEDGE CONFIRMATION
def confirm():
    if not session.logged_in_user:
        session.redirection = URL('bootable', 'confirm.html', vars=request.vars)
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    
    form = FORM(INPUT(_name='pledge_selection', _type='number'), INPUT(_name='bootable_id', _type='number'))
    if form.validate(formname="confirm"):
        user_pledges = db((db.bootable_pledges_made.pledge_id == db.bootable_pledges.id) & (db.bootable_pledges_made.user_id == session.logged_in_user) & (db.bootable_pledges.bootable_id == request.vars.bootable_id)).select()
        
        debug = open("DEBUG.txt", 'a')
        debug.write("Form submitted!\n")
        
        # If the user has already pledged to this bootable:
        if user_pledges:
            debug.write(str(user_pledges) + "\n")
            # Update the pledge.
            pledge = {'pledge_id': request.vars.pledge_selection, 'user_id': session.logged_in_user}
            db.bootable_pledges_made(user_pledges[0].bootable_pledges_made.id).update_record(**pledge)
        else:
            debug.write("User Pledges is falsey\n" + str(user_pledges) + "\n")
            # Add the pledge made to the database.
            pledge = {'pledge_id': request.vars.pledge_selection, 'user_id': session.logged_in_user}
            db.bootable_pledges_made.insert(**pledge)
            
        debug.close()
        # Redirect back to the bootable
        redirect(URL('bootable', 'view', vars={'bootable_id': db.bootable_pledges(request.vars.pledge_selection).bootable_id}))
    return dict(form=form, formkey=form.formkey)