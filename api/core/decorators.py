def authorize(email, password):
    def _check(func):
        def inner(self, *args, **kwargs):
            self.login_user(email, password)
            x = func(self, *args, **kwargs)
            self.clear_user()
            return x
        return inner
    return _check

def signature(params):
    def _check(func):
        def inner(self, *args, **kwargs):
            for key in params:
                if not getattr(self.cli_args, key, None):
                    self.logger.error("Test need Command line argument --%s to run" % key)
                    return

            return func(self, *args, **kwargs)
        return inner
    return _check
