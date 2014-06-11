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
    """
    Looks for parameters in Command Line Arguments.
    If CLI arg is missing. Runner will log an error and mark the test as OK.
    """
    def _check(func):
        def inner(self, *args, **kwargs):
            for key in params:
                if not getattr(self.cli_args, key, None):
                    self.logger.error("Test need Command line argument --%s to run" % key)
                    return

            return func(self, *args, **kwargs)
        return inner
    return _check
