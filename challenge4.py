class LockPicker_3MI0600342:
    def __init__(self, lock):
        self.lock = lock

    def unlock(self):
        args = []
        while True:
            try:
                if self.lock.pick(*args):
                    break
            except Exception as ex:
                if ex.position is None:
                    args = [None] * ex.expected
                elif isinstance(ex.expected, type):
                    args[ex.position - 1] = ex.expected()
                else:
                    args[ex.position - 1] = ex.expected