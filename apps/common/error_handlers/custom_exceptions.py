class DbLimitException(Exception):
    def __init__(self, message:str) -> None:
        """If you don't want to exceed certain number of entries this exception will be raised"""
        self.message = message
        super().__init__(message)
