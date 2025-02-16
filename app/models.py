from sqlmodel import Field, SQLModel
from enum import Enum


class YesNo(str, Enum):
    Yes = "Yes"
    No = "No"


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"


class Ethnicity(str, Enum):
    Caucasian = "Caucasian"
    Hispanic = "Hispanic"
    Asian = "Asian"
    African = "African"
    MiddleEastern = "Middle Eastern"


class ProfileBase(SQLModel):
    gender: Gender
    ethnicity: Ethnicity
    family_history: YesNo
    radiation_exposure: YesNo
    iodine_deficiency: YesNo
    smoking: YesNo
    nodule_size: float


class Profile(ProfileBase, table=True):
    id: int = Field(default=None, primary_key=True)
    diagnosis: str = Field(index=True)
