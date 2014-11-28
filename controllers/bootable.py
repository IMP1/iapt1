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
    # If we're deleting the bootable:
    if request.vars.bootable_deletion:
        # Delete the bootable.
        pass
    # If we're deleting a pledge:
    elif request.vars.pledge_deletion:
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
    
    # If we're updating the bootable:
    if form1.validate(formname="bootable"):
        if request.vars.bootable_deletion:
            session.flash = "'" + str(db.bootable(request.vars.bootable_deletion).title) + "' deleted."
            # Delete the bootable.
            db(db.bootable.id == int(request.vars.bootable_deletion)).delete()
            # Redirect as there's nothing left here now.
            redirect(URL('user', 'dashboard.html'))
        else:
            # Update
            response.flash = "Bootable updated!"
            # If we're updating and publishing:
            if request.vars.publish:
                # Publish
                record = db.bootable(request.vars.publish)
                updates = {'status_id': 2}
                record.update_record(**db.bootable._filter_fields(updates))
        
    # If we've used placeholders, put them back.
    for key in placeholders:
        request.vars[key] = placeholders[key]
        
    return dict(form1 = form1, form2 = form2, formkey1 = form1.formkey, formkey2 = form2.formkey)

## BOOTABLE PAGE VIEW
def view():
    return dict()

