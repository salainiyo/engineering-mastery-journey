from typing import List
from sqlmodel import SQLModel, Session, select, or_, col
from fastapi import APIRouter, Depends, Query, HTTPException
from app.models.services import MemberCreate, MemberUpdate, MemberPublic, Member, MemberDetailed, Loan
from app.database import get_session

member_router = APIRouter()

@member_router.post('/members/', response_model=MemberPublic, status_code=201)
def register_member(member: MemberCreate, session: Session = Depends(get_session)):
    new_member = Member.model_validate(member)
    try:
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) #to be corrected after tests to logging
    
@member_router.get('/members/search', response_model=list[MemberDetailed])
def search_members(
    q: str = Query(..., description="Search by name or phone number"),
    session: Session = Depends(get_session)
):
    statement = select(Member).where(
        or_(
            col(Member.first_name).contains(q),
            col(Member.last_name).contains(q),
            col(Member.phone_number).contains(q)
            
        )
    ).limit(10)
    
    results = session.exec(statement)
    return results

@member_router.get('/member/{id}', response_model=MemberDetailed)
def get_member_detailed(id: int, session: Session = Depends(get_session)):
    member = session.get(Member, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    active = [loan for loan in member.loans if loan.status == "active"]
    completed = [loan for loan in member.loans if loan.status == "paid"]
    
    return MemberDetailed.model_validate(
        member, 
        update={
            "active_loans": active, 
            "completed_loans": completed
        }
    )
    
@member_router.get("/members/detailed", response_model=List[MemberDetailed])
def get_all_members_detailed(session: Session = Depends(get_session)):
    members = session.exec(select(Member)).all()
    
    return [
        MemberDetailed.model_validate(
            m, 
            update={
                "active_loans": [l for l in m.loans if l.status == "active"],
                "completed_loans": [l for l in m.loans if l.status == "paid"]
            }
        ) for m in members
    ]