class BaseCallback:
    def __init__(self, app, args) -> None:
        self.app = app
        self.args = args