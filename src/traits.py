"""
This is a trait system draft based on soft dynamic inheritance

For exploration we would like to offer the Loggable trait for models so that the user can mark a class a 
loggable and specify the retreival field. It should act as a decorator over the class

"""

def Loggable(field='email'):
    def decorator(klass):
        class _Login:
            retreive_field: field
        klass._loggable = _Login
        return klass
    return decorator
