def dashboard():
    return dict()

def login():
    return dict()

# The User Registration Page
def new():
    # Create a form for the three tables
    form = SQLFORM.factory(db.user_address, db.user_credit_card, db.user)
    form.custom.widget.username["_placeholder"] = "Username"
    form.custom.widget.username["_class"] += " date-short"
    
    if form.process().accepted:
        id = db.client.insert(**db.client._filter_fields(form.vars))
        form.vars.client=id
        id = db.address.insert(**db.address._filter_fields(form.vars))
        response.flash='Thanks for filling the form'
    return dict(form = form)

def profile():
    return dict()