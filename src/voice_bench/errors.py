"""Failure ownership is explicit; a transport drop is not automatically simulator error."""


class CallerFailure(RuntimeError):
    pass


class HarnessFailure(RuntimeError):
    pass


class TransportFailure(RuntimeError):
    pass
