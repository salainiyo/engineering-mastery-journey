from sqlmodel import SQLModel, Session, select
from fastapi import APIRouter, Depends, Query, HTTPException
from app.models.services import MemberCreate, MemberUpdate, MemberPublic, Member, MemberAndLoan, Loan
from app.database import get_session

member_router = APIRouter()

@member_router.post('/member/', response_model=MemberPublic, status_code=201)
def register_member(member: MemberCreate, session: Session = Depends(get_session)):
    new_member = Member.model_validate(member)
    try:
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) #to be corrected after tests to logging
    
@member_router.get('/member/{id}', response_model=MemberAndLoan)
def get_member_and_loan(id: int, session: Session=Depends(get_session)):
    member = session.get(Member, id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member    