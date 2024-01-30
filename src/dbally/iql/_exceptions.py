import ast
from typing import Optional, Union


class IQLError(Exception):
    """Base exception for all IQL parsing related exceptions."""

    def __init__(self, message: str, node: Union[ast.stmt, ast.expr], source: str) -> None:
        message = message + ": " + source[node.col_offset : node.end_col_offset]

        super().__init__(message)
        self.node = node
        self.source = source


class IQLArgumentParsingError(IQLError):
    """Raised when an argument cannot be parsed into a valid IQL."""

    def __init__(self, node: Union[ast.stmt, ast.expr], source: str) -> None:
        message = "Not a valid IQL argument"
        super().__init__(message, node, source)


class IQLUnsupportedSyntaxError(IQLError):
    """Raised when trying to parse an unsupported syntax."""

    def __init__(self, node: Union[ast.stmt, ast.expr], source: str, context: Optional[str] = None) -> None:
        node_name = node.__class__.__name__

        message = f"{node_name} syntax is not supported in IQL"

        if context:
            message += " " + context

        super().__init__(message, node, source)
