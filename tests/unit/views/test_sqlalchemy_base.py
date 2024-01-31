# pylint: disable=missing-docstring, missing-return-doc, missing-param-doc, disallowed-name

import sqlalchemy

from dbally.iql import IQLActions, IQLQuery
from dbally.views.decorators import view_action, view_filter
from dbally.views.sqlalchemy_base import SqlAlchemyBaseView


class MockSqlAlchemyView(SqlAlchemyBaseView):
    """
    Mock class for testing the SqlAlchemyBaseView
    """

    def get_select(self) -> sqlalchemy.Select:
        return sqlalchemy.select(sqlalchemy.literal("test").label("foo"))

    @view_filter()
    def method_foo(self, idx: int) -> sqlalchemy.ColumnElement:
        """
        Some documentation string
        """
        return sqlalchemy.literal(idx)

    @view_filter()
    def method_bar(self, city: str, year: int) -> sqlalchemy.ColumnElement:
        return sqlalchemy.literal(f"hello {city} in {year}")

    @view_action()
    def action_baz(self, select: sqlalchemy.Select) -> sqlalchemy.Select:
        """
        This is baz
        """
        return select.order_by("foo")

    @view_action()
    def action_qux(self, select: sqlalchemy.Select, limit: int) -> sqlalchemy.Select:
        return select.limit(limit)


def test_filter_sql_generation() -> None:
    """
    Tests that the SQL generation based on filters works correctly
    """
    mock_view = MockSqlAlchemyView()
    query = IQLQuery.parse('method_foo(1) and method_bar("London", 2020)')
    mock_view.apply_filters(query)
    sql = mock_view.generate_sql().replace("\n", "")
    assert sql == "SELECT 'test' AS foo WHERE 1 AND 'hello London in 2020'"


def test_action_sql_generation() -> None:
    """
    Tests that the SQL generation based on actions works correctly
    """
    mock_view = MockSqlAlchemyView()
    actions = IQLActions.parse("action_baz()\naction_qux(5)")
    mock_view.apply_actions(actions)
    sql = mock_view.generate_sql().replace("\n", "")
    assert sql == "SELECT 'test' AS foo ORDER BY foo LIMIT 5"
