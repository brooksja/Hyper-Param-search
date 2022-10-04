########## Error handling ##########
class NoDataError(Exception):
    # Raised when critical data is missing
    def __init__(self,message='Critical data missing'):
        self.message = message
        super().__init__(self.message)

class BadPathError(Exception):
    # raised when a given path does not exist
    def __init__(self, message='Path does not exist'):
        self.message = message
        super().__init__(self.message)