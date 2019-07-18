class FeedsError(Exception):
    """
    Represents a generic exception with the Poller class.
    """
    pass


class InvalidPollerInterval(FeedsError):
    """
    The configured interval for polling is invalid.
    """
    pass


class EntryNotInDeluge(FeedsError):
    """
    A downloading show entry was not found in Deluge.
    """
    pass