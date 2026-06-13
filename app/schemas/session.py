from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SessionCreate(BaseModel):
	movie_id: int
	hall_id: int
	start_time: datetime


class SessionResponse(BaseModel):
	id: int
	movie_id: int
	hall_id: int
	start_time: datetime

	model_config = ConfigDict(from_attributes=True)