from typing import Annotated
from datetime import timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Request, HTTPException, Query, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

from sqlmodel import select

from app.core import *
from app.models import *
from app.schemas import *
from app.database import SessionDep, engine, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    yield
    
    engine.dispose() 

app = FastAPI(lifespan=lifespan)

def check_access_to_task(user: User, task: Task):
    if task.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail=f"User with id={user.id} do not have access to the task with id={task.id}"
        )

def get_task_by_id(session: SessionDep, task_id: int) -> Task | None:
    task = session.exec(select(Task).where(Task.id == task_id)).first()
    return task

def delete_task(session: SessionDep, task: Task) -> bool:
    session.delete(task)
    session.commit()
    return 0
    
def change_task(session: SessionDep,  task: Task, new_content: str) -> Task:
    task.task_content = new_content
    session.commit()
    session.refresh(task)
    return task
    
def switch_task(session: SessionDep,  task: Task) -> Task:
    task.is_complete = not task.is_complete
    session.commit()
    session.refresh(task)
    return task
    
# Endpoints section

@app.get("/help/", status_code=200, response_class=JSONResponse)
async def return_help_info():
    return {
        "Endpoints Available Query Parameters" : [
            {
                "/": {
                    "only_complete": "bool",
                    "only_uncomplete": "bool",
                    "limit": "int",
                    "page": "int",  
                },
            },
            {
                "/get/{task_id}/": {
                    "task_id": "int",  
                },
            },  
            {
                "/post/": {
                    "task_content": "list[str]",  
                },
            },  
            {
                "/delete/{task_id}/": {
                    "task_id": "int",  
                },
            },  
            {
                "/change/{task_id}/": {
                    "task_id": "int",
                    "task_content": "str",
                },
            },  
            {
                "/complete/{task_id}/": {
                    "task_id": "int",
                    "complete_val": "bool",
                },
            },  
            {
                "/logout/": {
                    "description": "Clears the access token cookie and redirects to /login/",
                    "params": "None"
                },
            },
        ]        
    }

@app.get("/login/", response_class=HTMLResponse)
async def give_login_page(request: Request):
    return """
    This page is for Log In into the server, after the loggining will send <br>
    a cookie access_token with JWT token and relocated to the main page.<br>
    If you are not previously registered into server - first visit /register/ for registration.
    <form action="/login/" method="post">
        <label for="username">Login:</label>
        <input type="text" id="username" name="username" placeholder="Enter a username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" placeholder="Enter a password" required><br>
        <input type="submit" value="Login"><br>
    </form>
        <a href="/register/">Go to a Registration page</a>
    """

@app.post("/login/", response_class=JSONResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta = access_token_expires 
    )
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key      = "access_token",
        value    = access_token,
        httponly = True,
        max_age  = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite = "Lax",
        path     = "/",
    )
    return response


@app.get("/logout/", response_class=RedirectResponse)
async def logout_user(user: UserDep):
    response = RedirectResponse(url="/login/", status_code=303)
    response.delete_cookie(
        key      = "access_token",
        httponly = True,
        samesite = "Lax",
        path     = "/",
    )
    return response

@app.get("/register/", response_class=HTMLResponse)
async def give_registration_page():
    return """
    This page is for Registration new users into the server, after the registration <br>
    you will get a cookie access_token with JWT token and relocated to the main page.
    <form action="/register/" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" placeholder="Enter username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" placeholder="Enter password" required><br>
        <label for="is_admin">Is an Admin? (for test):</label>
        <input type="checkbox" id="is_admin" name="is_admin"><br>
        <input type="submit" value="Register"><br>
    </form>
        <a href="/register/">Go to a Login page</a>
    """

@app.post("/register/", response_class=RedirectResponse)
async def registration(
        session:  SessionDep,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        is_admin: Annotated[bool, Form()] = False,
    ):
    
    if (get_user(session, username)):
        raise HTTPException(
            status_code = 409,
            detail      = f"Username {username} is already taken"
        )
    
    hashed_password = get_hash_password(password)
    new_user = User(
        username        = username,
        hashed_password = hashed_password,
        is_admin        = is_admin,
        is_disable      = False
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    new_user_pub: UserPublic = UserPublic(**new_user.model_dump(exclude={"hashed_password"}))
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data           = {"sub":username},
        expires_delta  = access_token_expires
    )

    if is_admin:
        pref = f"Admin"
    else:
        pref = "User"
    
    response = JSONResponse({"messsage": f"{pref} {new_user_pub.username} was created successfully",
                             "user": new_user_pub.model_dump()})
    response.set_cookie(
        key      = "access_token",
        value    = access_token,
        httponly = True,
        max_age  = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite = "Lax",
        path     = "/",
    )
    return response

@app.get("/get/{task_id}", status_code=200, response_class=JSONResponse)
async def get_task(
        user:    UserDep, 
        session: SessionDep, 
        task_id: int
    ):
    
    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code = 404,
            detail      = f"Task with id={task_id} not found"
        )

    check_access_to_task(user, task)

    return {
        "task": task.model_dump()
    }

@app.get("/", status_code=200, response_class=JSONResponse)
async def get_all_users_tasks(
        user:            UserDep,
        session:         SessionDep,
        only_complete:   Annotated[bool | None, Query(..., description = "Sorting tasks by complete val == true")] = None,
        only_uncomplete: Annotated[bool | None, Query(..., description = "Sorting tasks by complete val == false")] = None,
        limit:           Annotated[int  | None, Query(..., description = "Limit for amount of tasks in one page")] = None,
        page:            Annotated[int  | None, Query(..., description = "Page number of tasks")] = 1,
    ):

    if only_complete and only_uncomplete:
        raise HTTPException(
            status_code = 422,
            detail      = "Unprocessable queries: cannot generate response when only_complete and only_uncomplete == True. For more info visit /help/"
        )
    
    if limit == 0:
        raise HTTPException(
            status_code = 422,
            detail      = "Unprocessable queries: cannot generate response when amount of tasks in page limit = 0. For more info visit /help/"
        )

    statement = (
        (
            select(Task)
            .where(Task.user_id == user.id)
        )
    )

    if only_complete:     statement = statement.where(Task.is_complete == True)                            
    elif only_uncomplete: statement = statement.where(Task.is_complete == False)
    
    if limit: 
        offset    = (page - 1) * limit
        statement = statement.offset(offset=offset).limit(limit=limit)
        
    tasks_table = session.exec(statement).all()

    generated_res = [
        {
            "task_content": task.task_content,
            "is_complete":  task.is_complete,   
            "user_id":      user.id,
            "id" :          task.id
           }
        for task in tasks_table
        ]
    return {"tasks": jsonable_encoder(generated_res)}

@app.get("/post/", status_code=201)
async def post_tasks(
        user:         UserDep,
        session:      SessionDep,
        task_content: Annotated[
            list[str] | None, 
            Query(description="Content for task objects")
        ] = None,
    ):
    
    if task_content is None:
        raise HTTPException(
            status_code = 422,
            detail      = "Content for the Task was not given"
        )
    
    new_tasks = [
        Task(
            id           = None,
            is_complete  = False,
            user_id      = user.id,
            task_content = tc
        )
        for tc in task_content
    ]
    
    session.add_all(new_tasks)
    session.commit()
    for task in new_tasks:
        session.refresh(task)

    return {
        "message": f"{len(task_content)} tasks created successfully",
        "tasks":   [task.model_dump() for task in new_tasks]
    }


@app.get("/delete/{task_id}", status_code=200)
async def delete_task_by_id(
        user:    UserDep,
        session: SessionDep, 
        task_id: int
    ):

    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code = 404,
            detail      = f"Task with id={task_id} not found"
        )
    
    check_access_to_task(user, task)

    delete_task(session, task)
    return {"message": f"Task with id={task_id} deleted successfuly"}    
            

@app.get("/change/{task_id}/", status_code=200)
async def change_task_by_id(
        user:         UserDep,
        session:      SessionDep,
        task_id:      int,
        task_content: str = Query(..., description="Content for a task object")
    ):

    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code = 404,
            detail      = f"Task with id={task_id} not found"
        )
    
    check_access_to_task(user, task)
    new_task = change_task(session, task, task_content)
    return {
        "message": "Task chenged successfully",
        "task":    {
            "user_id":      new_task.user_id,
            "task_content": new_task.task_content,
            "complete":     new_task.is_complete,
            "id":           new_task.id,
        }
    }
    
@app.get("/switch/{task_id}/", status_code=200)
async def switch_task_by_id(
        user:    UserDep,
        session: SessionDep,
        task_id: int, 
    ):
    
    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code = 404,
            detail      = f"Task with id={task_id} not found"
        )
    
    check_access_to_task(user, task)
    new_task = switch_task(session, task)
    return {
        "message": "Task complete field switched successfully",
        "task":    {
            "user_id":      new_task.user_id,
            "task_content": new_task.task_content,
            "complete":     new_task.is_complete,
            "id":           new_task.id,
        }
    }