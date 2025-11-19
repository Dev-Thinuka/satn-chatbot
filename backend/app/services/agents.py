# backend/app/services/agents.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.agents import Agent
from app.schemas.agents import AgentCreate, AgentUpdate


def get_agents(db: Session, skip: int = 0, limit: int = 100) -> List[Agent]:
    return db.query(Agent).offset(skip).limit(limit).all()


def get_agent(db: Session, agent_id: int) -> Optional[Agent]:
    return db.query(Agent).filter(Agent.id == agent_id).first()


def create_agent(db: Session, agent_in: AgentCreate) -> Agent:
    agent = Agent(**agent_in.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


def update_agent(db: Session, agent_id: int, agent_in: AgentUpdate) -> Optional[Agent]:
    agent = get_agent(db, agent_id)
    if not agent:
        return None

    update_data = agent_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)

    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent
