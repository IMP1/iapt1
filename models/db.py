import os

# Create Database
db = DAL('sqlite://store.db')

# Database Tables
db.define_table('bootable_category', 
                    Field('name', 'string', requires=IS_NOT_EMPTY())
                )
db.define_table('bootable_status', 
                    Field('name', 'string', requires=IS_NOT_EMPTY())
                )
db.define_table('user_address', 
                    Field('street_address', 'string', requires=IS_NOT_EMPTY()),
                    Field('city', 'string', requires=IS_NOT_EMPTY()),
                    Field('country', 'string', requires=IS_NOT_EMPTY()),
                    Field('postcode', 'string', requires=[IS_NOT_EMPTY(), IS_LENGTH(7, 5)]),
                )
db.define_table('user_credit_card', 
                    Field('card_number', 'string', requires=[IS_NOT_EMPTY(), IS_LENGTH(12, 12)]),
                    Field('identifying_code', 'string', requires=[IS_NOT_EMPTY(), IS_LENGTH(3, 3)]),
                    Field('expiry_date', 'date'),
                    Field('billing_address_id', db.user_address),
                )
db.define_table('user', 
                    Field('username', 'string', requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'user.username')]),
                    Field('forename', 'string', requires=IS_NOT_EMPTY()),
                    Field('surname', 'string', requires=IS_NOT_EMPTY()),
                    Field('birthdate', 'date'),
                    Field('address_id', db.user_address),
                    Field('credit_card_id', db.user_credit_card),
                )
db.define_table('bootable', 
                    Field('title', 'string', requires=IS_NOT_EMPTY()), 
                    Field('category_id', db.bootable_category),
                    Field('summary', 'string', requires=IS_LENGTH(120)),
                    Field('description', 'text'),
                    Field('status_id', db.bootable_status),
                    Field('author', db.user),
                    Field('funding_goal', 'double', requires=IS_FLOAT_IN_RANGE(0, None)),
                    Field('image', 'upload', uploadfolder = os.path.join(request.folder, 'uploads')),
                    Field('about', 'text'),
                    Field('creation_date', 'datetime'),
                    # Available Pledges are referenced from `bootable_pledges`.
                    # Pledges made are referenced from `bootable_pledges_made`.
                )
db.define_table('bootable_published',
                    Field('bootable_id', db.bootable),
                    Field('publish_date', 'datetime'),
                )
db.define_table('bootable_pledges', 
                    Field('bootable_id', db.bootable),
                    Field('title', 'string', requires=IS_NOT_EMPTY()),
                    Field('cost', 'double', requires=IS_FLOAT_IN_RANGE(0, None)),
                    Field('reward', 'text'),
                    Field('include_previous_rewards', 'boolean'),
                )
db.define_table('bootable_pledges_made', 
                    Field('pledge_id', db.bootable_pledges),
                    Field('user_id', db.user),
                )

# Set up Bootable categories
if db(db.bootable_category.id > 0).count() == 0:
    db.bootable_category.insert(name = 'Art')
    db.bootable_category.insert(name = 'Comics')
    db.bootable_category.insert(name = 'Crafts')
    db.bootable_category.insert(name = 'Fashion')
    db.bootable_category.insert(name = 'Film')
    db.bootable_category.insert(name = 'Games')
    db.bootable_category.insert(name = 'Music')
    db.bootable_category.insert(name = 'Photography')
    db.bootable_category.insert(name = 'Technology')
    
# Set up Bootable statuses
if db(db.bootable_status.id > 0).count() == 0:
    db.bootable_status.insert(name = 'Not Available')
    db.bootable_status.insert(name = 'Open for Pledges')
    db.bootable_status.insert(name = 'Funded')
    db.bootable_status.insert(name = 'Not Funded')