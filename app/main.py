from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import user, auth, qrcodefun, workout


# models.Base.metadata.create_all(bind=engine)
# don't need this line anymore, since we now use alembic
# to automatically perfrom database edits

app = FastAPI()

origins = ["*"]  # ["*"] for public api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(qrcodefun.router)
app.include_router(workout.router)


@app.get("/")
async def root():
    return {"message": "hello world!!!!!!!!"}
