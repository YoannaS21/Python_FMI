class ProtectedSection:
    def __init__(self, log=(), suppress=()):
        self.log_elements = log
        self.suppress_elements = suppress
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            return False

        if isinstance(exc_value, self.log_elements):
            self.exception = exc_value
            return True

        if isinstance(exc_value, self.suppress_elements):
            return True

        return False

