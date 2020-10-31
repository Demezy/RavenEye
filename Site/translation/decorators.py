def check_session(func):
    def decorator(*args, **kwargs):
        if 'auth' not in args[0].session.keys():
            args[0].session['auth'] = 0
            print('Haven\'t auth key')
        return func(*args, **kwargs)
    return decorator
