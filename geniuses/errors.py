class Error(Exception):
    """Base error for this module."""

    pass


class UnauthorizedRequestError(Error):
    """Raised when the API token is not valid"""

    pass
