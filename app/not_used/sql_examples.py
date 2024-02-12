from typing import Optional, List
import fastapi
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="FastAPI",
            user="postgres",
            password="Shadow_Wizard_Money_Gang",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = fastapi.Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts


@app.post(
    "/create_post",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
async def create_post(post: schemas.PostCreate, db: Session = fastapi.Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = fastapi.Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    # if not post:
    #     raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
    #                                 detail=f"post with id: {id} was not found")

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@app.delete("/posts/{id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = fastapi.Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE ID = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # if not deleted_post:
    #     raise fastapi.HTTPException(
    #         status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    # conn.commit()

    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    if not deleted_post_query.first():
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist",
        )

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int, post: schemas.PostCreate, db: Session = fastapi.Depends(get_db)
):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = %s RETURNING *;""",
    #                 (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # if not updated_post:
    #     raise fastapi.HTTPException(
    #         status_code=fastapi.status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesn't exist")
    # conn.commit()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()

    if not updated_post:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist",
        )

    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post_query.first()


@app.post(
    "/users",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
async def create_user(user: schemas.UserCreate, db: Session = fastapi.Depends(get_db)):
    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = fastapi.Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} does not exist",
        )

    return user
