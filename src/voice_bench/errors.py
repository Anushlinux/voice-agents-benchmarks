"""Failure ownership is explicit; a transport drop is not automatically simulator error."""


class CallerFailure(RuntimeError):
    pass


class HarnessFailure(RuntimeError):
    pass


class TransportFailure(RuntimeError):
    pass


class ConversationTimeout(TransportFailure):
    """A local patience limit expired; this does not establish a network fault."""
