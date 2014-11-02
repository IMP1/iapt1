db = DAL('sqlite://store.db')

db.define_table('products', 
                Field('name'), 
                Field('price'), 
                Field('type'), 
                Field('description'), 
                Field('publisher')
               )
db.define_table('features', 
                Field('product_id', db.products)
               )