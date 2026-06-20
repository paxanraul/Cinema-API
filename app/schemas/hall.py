from pydantic import BaseModel, ConfigDict

class HallCreate(BaseModel):
	name: str
	capacity: int
	location: str


class HallResponse(BaseModel):
	id: int
	name: str
	capacity: int
	location: str
	is_active: bool

	model_config = ConfigDict(from_attributes=True)