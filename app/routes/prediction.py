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
        {
            "Age": [66],
            "Gender": [profile_data.gender.value],
            "Country": ["Russia"],
            "Ethnicity": [profile_data.ethnicity.value],
            "Family_History": [profile_data.family_history.value],
            "Radiation_Exposure": [profile_data.radiation_exposure],
            "Iodine_Deficiency": [profile_data.iodine_deficiency],
            "Smoking": [profile_data.smoking],
            "Obesity": [profile_data.smoking],
            "Diabetes": [profile_data.smoking],
            "TSH_Level": [9.37],
            "T3_Level": [1.67],
            "T4_Level": [6.16],
            "Nodule_Size": [profile_data.nodule_size],
            "Thyroid_Cancer_Risk": ["Low"],
        },
    )
    pipeline = joblib.load("pipeline.pkl")
    prediction = pipeline.predict(df)
    if prediction[0] == 0:
        diagnosis = "Negative"
    elif prediction[0] == 1:
        diagnosis = "Positive"
    else:
        diagnosis = "Unknown"

    profile = Profile(**profile_data.model_dump(), diagnosis=diagnosis)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("", response_model=list[Profile])
def get_predictions(session: SessionDep):
    predictions = session.exec(select(Profile)).all()
    return predictions
