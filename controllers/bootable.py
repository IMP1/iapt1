def search():
    search_vars = request.vars
    return dict(search_vars = search_vars)

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
    
    # If the third form has been submitted:
    if form3.validate(formname='pledges') and request.vars.creation_stage == 2:
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
                redirect(URL('bootable', 'edit.html', vars = dict(bootable=target)))
        else:
            session.flash = "Pledge added!"
            # Add the pledge.
            db.bootable_pledges.insert(**db.bootable_pledges._filter_fields(form3.vars))
            # Don't go anywhere because more pledges can be added.
    # If we've clicked on finish, we don't need the form to be filled out.
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
    
    forms = [form1, form2, form3]
    stage = request.vars.creation_stage
    return dict(form = forms[stage], stage = stage, formkey = forms[stage].formkey)


def edit():
    if not session.logged_in_user:
        session.redirection = URL('bootable', 'edit.html')
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

def view():
    return dict()

