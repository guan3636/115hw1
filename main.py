from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db import getDB, lifespan

# from routes import router as all_routes
# from routes.upload import router as upload_router
# from routes import users

templates = Jinja2Templates(directory="templates")
app = FastAPI(lifespan=lifespan)


# app.include_router(all_routes, prefix="/")

@app.get("/students/list")
async def read_users(db=Depends(getDB)):
    cur = await db.execute("SELECT * FROM students")
    return await cur.fetchall()

@app.get("/students/list/template")
async def stuList(request: Request, db=Depends(getDB)):
    cur = await db.execute("SELECT * FROM students order by stuid;")
    data = await cur.fetchall()
    return templates.TemplateResponse(
        name="studentList.html", 
        request=request, 
        context={"students": data}
    )
@app.get("/student/delete/{stuid}")
async def stuDelete(stuid: int, db=Depends(getDB)):
    await db.execute("DELETE FROM students WHERE stuid=%s;", (stuid,))
    return RedirectResponse(url="/students/list/template", status_code=303)

@app.get("/student/create/template")
async def stuCreateForm(request: Request):
    return templates.TemplateResponse(name="studentCreate.html", request=request)

@app.post("/student/create")
async def stuCreate(stuid: int = Form(...), name: str = Form(...), height: int = Form(...), db=Depends(getDB)):
    await db.execute("INSERT INTO students (stuid, name, height) VALUES (%s, %s, %s);", (stuid, name, height))
    return RedirectResponse(url="/students/list/template", status_code=303)