
class InvalidTokenError(ValueError):
    pass


class UserNotFoundError(ValueError):
    def __int__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found")

class InvalidUserCredentials(ValueError):
    pass


class DuplicatePasswordError(ValueError):
    pass
