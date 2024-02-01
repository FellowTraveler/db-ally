import typing


def view_filter() -> typing.Callable:
    """
    Decorator for marking a method as a filter

    :return: Function that returns the decorated method
    """

    def wrapped(func: typing.Callable) -> typing.Callable:  # pylint: disable=missing-return-doc
        func._methodDecorator = view_filter  # type:ignore # pylint: disable=protected-access
        return func

    return wrapped


def view_action() -> typing.Callable:
    """
    Decorator for marking a method as an action

    :return: Function that returns the decorated method
    """

    def wrapped(func: typing.Callable) -> typing.Callable:  # pylint: disable=missing-return-doc
        func._methodDecorator = view_action  # type: ignore # pylint: disable=protected-access
        return func

    return wrapped
