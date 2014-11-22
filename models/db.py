db = DAL('sqlite://store.db')

db.define_table('bootable_category', 
                    Field('name', 'string', requires=IS_NOT_EMPTY())
                )
db.define_table('bootable_status', 
                    Field('name', 'string', requires=IS_NOT_EMPTY())
                )
db.define_table('bootable', 
                    Field('title', 'string', requires=IS_NOT_EMPTY()), 
                    Field('summary', 'string', requires=IS_LENGTH(120)),
                    Field('category_id', db.bootable_category),
                    Field('status_id', db.bootable_status),
                    Field('fundingGoal', 'double', requires=IS_FLOAT_IN_RANGE(0, 1e100)),
                    Field('image', 'upload'),
                    Field('description', 'text'),
                    Field('about', 'text'),
                    # Available Pledges are referenced from `bootable_pledges`.
                    # Pledges made are referenced from `bootable_pledges_made`.
                )
db.define_table('bootable_pledges', 
                    Field('bootable_id', db.bootable),
                    Field('title', 'string', requires=IS_NOT_EMPTY()),
                    Field('cost', 'double', requires=IS_FLOAT_IN_RANGE(0, 1e100)),
                    Field('reward', 'text'),
                )
db.define_table('user_address', 
                    Field('street_address', 'string', requires=IS_NOT_EMPTY()),
                    Field('city', 'string', requires=IS_NOT_EMPTY()),
                    Field('country', 'string', requires=IS_NOT_EMPTY()),
                    Field('postcode', 'string', requires=IS_LENGTH(7)),
                )
db.define_table('user_credit_card', 
                    Field('card_number', 'string', requires=IS_LENGTH(12)),
                    Field('identifying_code', 'string', requires=IS_LENGTH(3)),
                    Field('expiry_date', 'date'),
                    Field('billing_address_id', db.user_address),
                )
db.define_table('user', 
                    Field('username', 'string', requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'user.username')]),
                    Field('real_name', 'string', requires=IS_NOT_EMPTY()),
                    Field('birthdate', 'date'),
                    Field('address_id', db.user_address),
                    Field('credit_card_id', db.user_credit_card),
                    
                )
db.define_table('bootable_pledges_made', 
                    Field('pledge_id', db.bootable_pledges),
                    Field('user_id', db.user),
                )
