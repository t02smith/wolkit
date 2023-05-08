
class InvalidTokenError(ValueError):
    pass


class UserNotFoundError(ValueError):
    pass


class InvalidUserCredentials(ValueError):
    pass


class DuplicatePasswordError(ValueError):
    pass
