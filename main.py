from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from my_config import get_db
from database import engine, Base, Sessionlocal
from model.users import UserCreate, Users, LoginInput
from model.task import Task, TaskCreate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

user_ops = Users()
taskObj = Task()

Base.metadata.create_all(bind=engine)


@app.post('/api/login')
def login(request: Request, credential: LoginInput):
    return user_ops.login(request, credential)


@app.post("/api/insert/register")
async def register(data: UserCreate, request: Request, db: Session = Depends(get_db)):
    return user_ops.register(data.model_dump(), request, db)


@app.get('/api/is-registered')
def is_registered(mob_no: int):
    return user_ops.is_registered(mob_no)


###################################################################################
@app.post('/api/task-insert')
def task_insert(data: TaskCreate, db: Sessionlocal = Depends(get_db)):
    return taskObj.task_insert(data.model_dump(), db)


@app.get('/app/task-read')
def task_read(uuid: str = None, db: Sessionlocal = Depends(get_db)):
    return taskObj.task_read(uuid, db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000)
