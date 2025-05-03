from sqlmodel import SQLModel, Field

class Constellation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    scientific_name: str
    general_names: str
    star_coords: str

