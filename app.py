import uvicorn
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel


from routers import cars, web
from db import engine

app = FastAPI(title="Car Sharing")
app.include_router(cars.router)
app.include_router(web.router)
app.add_middleware(CORSMiddleware, allow_origins=['*'])


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.middleware("http")
async def add_cars_cookie(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time()-start)
    response.set_cookie(key="cars_cookie", value="you visited the car searching app")
    return response


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
