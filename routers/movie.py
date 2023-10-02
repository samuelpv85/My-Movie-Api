from typing import List, Optional
from fastapi import Depends, Path, Query, status
from pydantic import BaseModel, Field
from middlewares.jwt_beaber import JWTBearer
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Path, Query, status
from typing import List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from models.movie import Movie as MovieModel
from services.movie import MovieService
from schemas.movie import Movie

movie_route = APIRouter()

# @movie_route.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])


@movie_route.get("/movies", tags=["movies"], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies() -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).all()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@movie_route.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first()
    # ejecuta la consulta desde services
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No Encontrado"})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_route.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15,
                          title="Categoria Movie",
                          description="This is the movie category")) -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.category == category).all()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No Encontrado"})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_route.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    # new_movie = MovieModel(**movie.dict())
    # db.add(new_movie)
    # db.commit()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "se ha registrado la pelicula"}, status_code=201)


@movie_route.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    db = Session()
    # result = db.query(MovieModel).where(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    if result:
        MovieService(db).update_movie(id, movie)
        return JSONResponse(status_code=201, content={"message": "Updated done"})

    if not result:
        return JSONResponse(status_code=404, content={'message': 'ID No found'})


@movie_route.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:

    db = Session()
    # result = db.query(MovieModel).where(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    print(jsonable_encoder(result))  # prueba imprimir en el logs
    if result:
        MovieService(db).delete_movie(id)
        return JSONResponse(status_code=200, content={"message": "Record deleted"})

    if not result:
        return JSONResponse(status_code=404, content={'message': 'ID No found'})
