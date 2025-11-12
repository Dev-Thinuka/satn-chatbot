from pydantic import BaseModel
class PropertyOut(BaseModel):
    id: str
    title: str
    description: str | None = None
    price: float | None = None
    location: str | None = None
    features: dict | None = None
    agent_id: str | None = None
