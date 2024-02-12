from passlib.context import CryptContext
import hashlib
from random import randint

# emailing stuff
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_hashes(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_verification_code():
    verification_code = str(randint(1000, 9999))
    # token = randbytes(2)

    # hashedCode = hashlib.sha256()
    # hashedCode.update(token)

    # verification_code = hashedCode.hexdigest()
    return verification_code


def send_email(sender_email, recepient_email, subject, data_transfered, password):
    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = recepient_email
    msg["Subject"] = subject

    message = data_transfered
    msg.attach(MIMEText(message, "plain"))

    smtpObj = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    smtpObj.login(sender_email, password)

    smtpObj.send_message(msg=msg, from_addr=msg["From"], to_addrs=msg["To"])
    smtpObj.quit()
