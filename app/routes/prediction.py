from fastapi import APIRouter, Depends
from ..models import ProfileBase, Profile
from ..database import SessionDep
import pandas as pd

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("", response_model=Profile)
def predict(profile_data: ProfileBase, session: SessionDep):
    df = pd.DataFrame({"family_history": profile_data.family_history})
    # pipeline.predict(df)
    profile = Profile(**profile_data.model_dump(), diagnosis="Negative")
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get("", response_model=list[Profile])
def get_predictions(session: SessionDep):
    predictions = session.exec(select(Profile)).all()
    return predictions
