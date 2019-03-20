
def check_opened(func, *args):
    def new_func(*args):
        if args[0]._file is not None:
            return func(*args)
        else:
            raise Exception()
    return new_func
