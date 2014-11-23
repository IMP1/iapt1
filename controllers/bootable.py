def search():
    search_vars = request.vars
    return dict(search_vars = search_vars)

def create():
    if not session.logged_in_user:
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

def edit():
    if not session.logged_in_user:
        session.flash = SPAN('You are not currently signed in. Sign in or ', A('Register', _href=URL('user', 'new.html')), '!')
        redirect(URL('user', 'login.html'))
    return dict()

def view():
    return dict()

