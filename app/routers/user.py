import fastapi
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=fastapi.status.HTTP_201_CREATED, response_model=schemas.UserOut
)
async def create_user(user: schemas.UserCreate, db: Session = fastapi.Depends(get_db)):
    find_user = db.query(models.User).filter(models.User.email == user.email).first()
    if find_user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с почтой {user.email} уже существует",
        )

    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = fastapi.Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id {id} не существует",
        )

    return user
