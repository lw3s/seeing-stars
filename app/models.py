from sqlmodel import SQLModel, Field

class Constellation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    scientific_name: str
    informal_name: str
    star_coords: str

