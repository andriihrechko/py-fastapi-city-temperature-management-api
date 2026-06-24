from sqlalchemy import select

from app.models.city import CityModel
from app.database.config import DatabaseSession
from app.schemas.city import CityCreateSchema, CityUpdateSchema


def retrieve_city(db: DatabaseSession, city_id: int) -> CityModel | None:
    stmt = select(CityModel).where(CityModel.id == city_id)
    return db.scalars(stmt).first()


def retrieve_city_by_name(
    db: DatabaseSession, city_name: str
) -> CityModel | None:
    stmt = select(CityModel).where(CityModel.name == city_name)
    return db.scalars(stmt).first()


def list_cities(db: DatabaseSession) -> list[CityModel]:
    stmt = select(CityModel)
    return db.scalars(stmt).all()


def create_city(db: DatabaseSession, city: CityCreateSchema) -> CityModel:
    city = CityModel(**city.model_dump())
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def update_city(
    db: DatabaseSession, city_id: int, city: CityUpdateSchema
) -> CityModel:
    db_city = db.get(CityModel, city_id)
    update_data = city.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: DatabaseSession, city_id: int) -> None:
    city = retrieve_city(db=db, city_id=city_id)
    db.delete(city)
    db.commit()
