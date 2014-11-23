def search():
    search_vars = request.vars
    return dict(search_vars = search_vars)

def create():
    if not session.logged_in_user:
        redirect(URL('default', 'index.html'))
    return dict()

def edit():
    if not session.logged_in_user:
        redirect(URL('default', 'index.html'))
    return dict()

def view():
    return dict()

