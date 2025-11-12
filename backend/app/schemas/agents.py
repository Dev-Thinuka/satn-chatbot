from pydantic import BaseModel
class AgentOut(BaseModel):
    id: str
    name: str
    role: str | None = None
    contact_info: dict | None = None
