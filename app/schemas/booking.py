from pydantic import BaseModel, ConfigDict

class BookingCreate(BaseModel):
	session_id: int


class BookingResponse(BaseModel):
	id: int
	session_id: int
	user_id: int
	status: str
	is_active: bool

	model_config = ConfigDict(from_attributes=True)