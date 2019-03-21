
def check_opened(func):
    def new_func(*args):
        if args[0].get_file() is not None and not args[0].get_file().closed:
            return func(*args)
        else:
            raise FileNotFoundError()
    return new_func
