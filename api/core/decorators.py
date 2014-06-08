def authorize(email, password):
    def _check(func):
        def inner(self, *args, **kwargs):
            self.login_user(email, password)
            x = func(self, *args, **kwargs)
            self.clear_user()
            return x
        return inner
    return _check
