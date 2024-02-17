import fastapi
from datetime import datetime
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = fastapi.APIRouter(prefix="/workout", tags=["Workout"])


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED)
def create_workout(
    info: schemas.CreateWorkout,
    db: Session = fastapi.Depends(get_db),
    current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user),
):
    info: dict = info.model_dump()
    info.update({"user_id": current_user.id})

    new_workout = models.Workout(**info)
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout


@router.put("/{workout_id}", status_code=fastapi.status.HTTP_202_ACCEPTED)
def end_workout(
    workout_id: int,
    db: Session = fastapi.Depends(get_db),
    current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user),
):
    workout_to_end_query = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    )
    workout_to_end = workout_to_end_query.first()

    if workout_to_end.user_id != current_user.id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    workout_to_end_query.update({"ended_at": datetime.now()})
    db.commit()
    return {"message": "Workout ended successfully"}


@router.post("/{workout_id}/exercise", status_code=fastapi.status.HTTP_201_CREATED)
def add_set(
    workout_id: int,
    title: schemas.AddExercise,
    db: Session = fastapi.Depends(get_db),
    current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user),
):
    new_exercise_dict = title.model_dump()
    new_exercise_dict.update({"workout_id": workout_id})
    new_exercise = models.IndividualExercise(**new_exercise_dict)
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise


@router.post("/set/{exercise_id}", status_code=fastapi.status.HTTP_201_CREATED)
def add_set(
    exercise_id: int,
    set_info: schemas.AddSet,
    db: Session = fastapi.Depends(get_db),
    current_user: schemas.UserOut = fastapi.Depends(oauth2.get_current_user),
):
    new_set_dict = set_info.model_dump()
    new_set_dict.update({"exercise_id": exercise_id})
    new_exercise = models.Set(**new_set_dict)
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise
