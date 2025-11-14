# backend/app/api/v1/agents.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.agents import AgentRead, AgentCreate, AgentUpdate
from app.services import agents as agents_service

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.get("", response_model=List[AgentRead], summary="List all agents")
def list_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return agents_service.get_agents(db=db, skip=skip, limit=limit)


@router.get("/{agent_id}", response_model=AgentRead, summary="Get agent by ID")
def get_agent_by_id(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = agents_service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    return agent


@router.post(
    "",
    response_model=AgentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create agent",
)
def create_agent(
    payload: AgentCreate,
    db: Session = Depends(get_db),
):
    # Later: protect with admin auth
    agent = agents_service.create_agent(db, payload)
    return agent


@router.put("/{agent_id}", response_model=AgentRead, summary="Update agent")
def update_agent(
    agent_id: int,
    payload: AgentUpdate,
    db: Session = Depends(get_db),
):
    agent = agents_service.update_agent(db, agent_id, payload)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )
    return agent
