from fastapi import APIRouter, HTTPException

from app.database.config import DatabaseSession
from app.schemas.city import CitySchema, CityCreateSchema, CityUpdateSchema
from app.services.city import (
    retrieve_city,
    list_cities,
    retrieve_city_by_name,
    create_city,
    update_city,
    delete_city,
)

router = APIRouter(
    prefix="/cities",
    tags=["Cities API"],
)


@router.get(
    "/{city_id}/",
    response_model=CitySchema,
)
def get_city_api(db: DatabaseSession, city_id: int):
    city = retrieve_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.get(
    "/",
    response_model=list[CitySchema],
)
def get_cities_api(db: DatabaseSession):
    return list_cities(db=db)


@router.post("/", response_model=CitySchema)
def create_city_api(db: DatabaseSession, city: CityCreateSchema):
    db_city = retrieve_city_by_name(db=db, city_name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists.")
    return create_city(db=db, city=city)


@router.patch("/{city_id}/", response_model=CitySchema)
def update_city_api(db: DatabaseSession, city_id: int, city: CityUpdateSchema):
    db_city = retrieve_city_by_name(db=db, city_name=city.name)
    if db_city and db_city.id != city_id:
        raise HTTPException(status_code=400, detail="City already exists.")
    db_city = retrieve_city(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    return update_city(db=db, city_id=city_id, city=city)


@router.delete("/{city_id}/")
def delete_city_api(db: DatabaseSession, city_id: int):
    city = retrieve_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found.")
    delete_city(db=db, city_id=city_id)
    return {"message": "City deleted successfully."}
