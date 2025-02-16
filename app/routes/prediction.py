from fastapi import APIRouter, Depends
from ..models import ProfileBase, Profile
from ..database import SessionDep
import pandas as pd
from sqlmodel import select
import joblib

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("", response_model=Profile)
def predict(profile_data: ProfileBase, session: SessionDep):
    df = pd.DataFrame(
        {"gender": [profile_data.gender.value]},
        {"ethnicity": [profile_data.ethnicity.value]},
        {"family_history": [profile_data.family_history.value]},
        {"radiation_exposure": [profile_data.radiation_exposure]},
        {"iodine_deficiency": [profile_data.iodine_deficiency]},
        {"smoking": [profile_data.smoking]},
        {"nodule_size": [profile_data.nodule_size]},
    )
    pipeline = joblib.load("pipeline.pkl")
    pipeline.predict(df)
    profile = Profile(**profile_data.model_dump(), diagnosis="Negative")
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("", response_model=list[Profile])
def get_predictions(session: SessionDep):
    predictions = session.exec(select(Profile)).all()
    return predictions
