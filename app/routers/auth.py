from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from ..config import settings


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильная почта или пароль",
        )

    if not utils.verify_hashes(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильная почта или пароль",
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@router.post("/password-reset")
async def email_reset(
    recepient_email: schemas.UserVerifyEmail, db: Session = Depends(database.get_db)
):
    user_query = db.query(models.User).filter(
        models.User.email == recepient_email.email
    )
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не существует"
        )

    try:
        verification_code = utils.create_verification_code()

        sender_email = settings.smtp_email
        sender_password = settings.smtp_password

        utils.send_email(
            sender_email,
            recepient_email.email,
            "Verification",
            verification_code,
            sender_password,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Произошла ошибка в отправке сообщения на электронную почту",
        )

    user_query.update(
        {"verification_code": verification_code}, synchronize_session=False
    )
    db.commit()

    return {"message": f"Код подтверждения отправлен на почту {recepient_email.email}"}


@router.get("/password-reset")
async def verify_code_email(
    verification_code: int, email: str, db: Session = Depends(database.get_db)
):
    check_validity_query = db.query(models.User).filter(
        models.User.verification_code == verification_code, models.User.email == email
    )
    check_validity = check_validity_query.first()

    if not check_validity:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильный код подтверждения",
        )

    return {"message": "Верный код"}


@router.put("/password-reset")
async def reset_password(
    data: schemas.ResetPassword, db: Session = Depends(database.get_db)
):
    email = data.email
    verification_code = data.verification_code
    password_to_change = data.password

    user_query = db.query(models.User).filter(
        models.User.email == email, models.User.verification_code == verification_code
    )

    user_query.update(
        {"password": utils.hash(password_to_change), "verification_code": None}
    )
    db.commit()

    return {"message": "Пароль успешно изменён"}
