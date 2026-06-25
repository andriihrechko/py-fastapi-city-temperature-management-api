from fastapi import APIRouter

from app.database.config import DatabaseSession
from app.schemas.temperature import TemperatureSchema
from app.services.temperature import update_all_temperatures, list_temperatures

router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures API"],
)


@router.post("/update")
async def update_temperatures(db: DatabaseSession):
    count = await update_all_temperatures(db=db)
    return {"message": f"{count} Temperatures updated successfully."}


@router.get("/", response_model=list[TemperatureSchema])
def read_temperatures(db: DatabaseSession, city_id: int = None):
    return list_temperatures(db=db, city_id=city_id)
