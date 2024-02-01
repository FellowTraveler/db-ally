# pylint: disable=missing-docstring, missing-return-doc, missing-param-doc
import asyncio

import pandas as pd
import sqlalchemy
from config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import dbally
from dbally import SqlAlchemyBaseView, decorators

engine = create_engine(config.pg_connection_string + "/superhero")
SuperheroModel = automap_base()
SuperheroModel.prepare(autoload_with=engine, reflect=True)


class SuperheroView(SqlAlchemyBaseView):
    """
    View used as an example
    """

    def __init__(self) -> None:
        super().__init__()
        self._subquery: sqlalchemy.sql.selectable.Subquery

    def get_select(self) -> sqlalchemy.Select:
        """
        Creates the initial SqlAlchemy select object, which will be used to build the query.
        """
        select = sqlalchemy.select(SuperheroModel.classes.superhero)
        self._subquery = select.alias("main_view")
        return sqlalchemy.select("*").select_from(self._subquery)

    @decorators.view_filter()
    def filter_by_superhero_name(self, name: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.superhero_name == name

    @decorators.view_filter()
    def filter_by_eye_color(self, color: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.eye_colour_id.in_(
            sqlalchemy.select(SuperheroModel.classes.colour.id).where(SuperheroModel.classes.colour.colour == color)
        )

    @decorators.view_filter()
    def filter_by_hair_color(self, color: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.hair_colour_id.in_(
            sqlalchemy.select(SuperheroModel.classes.colour.id).where(SuperheroModel.classes.colour.colour == color)
        )

    @decorators.view_filter()
    def filter_by_skin_color(self, color: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.skin_colour_id.in_(
            sqlalchemy.select(SuperheroModel.classes.colour.id).where(SuperheroModel.classes.colour.colour == color)
        )

    @decorators.view_filter()
    def filter_by_race(self, race: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.race_id.in_(
            sqlalchemy.select(SuperheroModel.classes.race.id).where(SuperheroModel.classes.race.race == race)
        )

    @decorators.view_filter()
    def filter_by_publisher(self, publisher: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.publisher_id.in_(
            sqlalchemy.select(SuperheroModel.classes.publisher.id).where(
                SuperheroModel.classes.publisher.publisher == publisher
            )
        )

    @decorators.view_filter()
    def filter_by_alignment(self, alignment: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.alignment_id.in_(
            sqlalchemy.select(SuperheroModel.classes.alignment.id).where(
                SuperheroModel.classes.alignment.alignment == alignment
            )
        )

    @decorators.view_filter()
    def filter_by_gender(self, gender: str) -> sqlalchemy.ColumnElement:
        return self._subquery.c.gender_id.in_(
            sqlalchemy.select(SuperheroModel.classes.gender.id).where(SuperheroModel.classes.gender.gender == gender)
        )

    @decorators.view_filter()
    def heavier_than(self, weight: float) -> sqlalchemy.ColumnElement:
        return self._subquery.c.weight_kg > weight

    @decorators.view_filter()
    def lighter_than(self, weight: float) -> sqlalchemy.ColumnElement:
        return self._subquery.c.weight_kg < weight

    @decorators.view_filter()
    def taller_than(self, height: float) -> sqlalchemy.ColumnElement:
        return self._subquery.c.height_cm > height

    @decorators.view_filter()
    def shorter_than(self, height: float) -> sqlalchemy.ColumnElement:
        return self._subquery.c.height_cm < height

    @decorators.view_action()
    def sort_by_gender(self, select: sqlalchemy.Select) -> sqlalchemy.Select:
        return select.order_by(self._subquery.c.gender_id)


async def main():
    superheros_db = dbally.create_collection("superheros_db")
    superheros_db.add(SuperheroView)

    response = await superheros_db.ask("What heroes have blue eyes and are taller than 180cm?")
    print(response)
    print(pd.read_sql_query(response, engine))


if __name__ == "__main__":
    asyncio.run(main())
