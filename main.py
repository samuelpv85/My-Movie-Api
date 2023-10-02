from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandle
from routers.movie import movie_route
from routers.user import user_router

# app = FastAPI()
app = FastAPI(
    title="My app with FastAPI",
    description="Aprove using api",
    version="0.1.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Samuel Patiño",
        "url": "https://github.com/joelbarranteswins/Platzi-Courses",
        "email": "sp@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}

)
# midd a nivel general de la app
app.add_middleware(ErrorHandle)
app.include_router(movie_route)
app.include_router(user_router)

# motor donde se crearan las tablas
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
