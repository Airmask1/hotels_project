class ObjectNotFoundError(Exception):
    """Raised when an object is not found in the database."""

    pass


class MultipleObjectsFoundError(Exception):
    """Raised when multiple objects are found when expecting one."""

    pass


class UserAlreadyExists(Exception):
    pass
