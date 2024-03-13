import csv
from pathlib import Path
from typing import Dict, Optional

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

import dbally

ENGINE = create_engine("sqlite://")
PATH_PACKAGE = Path(dbally.__file__).parent


class Base(DeclarativeBase):
    """
    This class represents the base of the recruitment database.
    """


class Candidate(Base):
    """
    This class represents the candidate table in the recruitment database.
    """

    __tablename__ = "candidate"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str]
    years_of_experience: Mapped[int]
    position: Mapped[str]
    university: Mapped[str]
    skills: Mapped[str]
    tags: Mapped[str]

    def __repr__(self) -> str:
        return f"Candidate(id={self.id!r}, name={self.name!r}, country={self.country!r},\
            years_of_experience={self.years_of_experience!r}, position={self.position!r},\
            university={self.university!r}), skills={self.skills!r}, tags={self.tags!r})"


Base.metadata.create_all(ENGINE)


def fill_candidate_table() -> None:
    """
    Fills the candidate table with data from the dbally/examples/recruiting.csv file.
    """
    with Session(ENGINE) as session:
        candidates = []
        with open(PATH_PACKAGE / "examples" / "recruiting.csv", newline="", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                candidate = Candidate(
                    id=i,
                    name=row["name"],
                    country=row["country"],
                    years_of_experience=row["years_of_experience"],
                    position=row["position"],
                    university=row["university"],
                    skills=row["skills"],
                    tags=row["tags"],
                )
                candidates.append(candidate)

        session.add_all(candidates)
        session.commit()


def get_recruitment_db_description(descriptions: Optional[Dict[str, str]] = None) -> str:
    """Generates a description of the recruitment database.

    Args:
        descriptions (Dict[str, str]): A dictionary with column names as keys and their descriptions as values.

    Returns:
        str: A description of the recruitment database.
    """
    if descriptions is None:
        descriptions = {
            "id": "Unique identifier of the candidate",
            "name": "Name of the candidate",
            "country": "Country of the candidate",
            "years_of_experience": "Years of experience of the candidate",
            "position": "Position of the candidate",
            "university": "University of the candidate",
        }

    metadata = MetaData()
    metadata.reflect(bind=ENGINE)

    db_description = ""
    for table in metadata.tables.values():
        db_description += f"Table: {table.name}\n"
        for column in table.c:
            db_description += f"  {column.name}[{column.type}]: {descriptions.get(column.name, 'No description')}\n"

    return db_description
