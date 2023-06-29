""" 
We need a solid used system for login, we don't really want to bake our own with the risk that comes with it, 
or we would need to invest a lot and become deeply expert in the subject
"""

import bcrypt
import inflect
from ..utils.hiddenid import int_to_hash
from ..utils.pg import get_db_sync
from ..response import Response
pluralize = inflect.engine().plural

def make_login(app, model):

    name = model.__name__
    
    plural_name = pluralize(name)
    
    model_db_sync = get_db_sync(model)
    
    
    @app.post(f"/{plural_name}/login")
    def login(user: model):
        #get model
        model_db_sync[model._Login.retreive_field]
        #check password
        bcrypt.checkpw(user.password)
        #session state changes + jwt token
        ...