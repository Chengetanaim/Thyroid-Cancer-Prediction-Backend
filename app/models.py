from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    family_history: str = Field(index=True)


class Profile(ProfileBase, table=True):
    id: int = Field(default=None, primary_key=True)
    diagnosis: str = Field(index=True)
