from sqlmodel import SQLModel, Session, select
from fastapi import APIRouter, Depends, Query, HTTPException
from app.models.services import CreateLoan, UpdateLoan, PublicLoan, Loan, Member
from app.database import get_session

loan_router = APIRouter()

@loan_router.post('/loan/{member_id}', response_model=PublicLoan, status_code=201)
def register_loan(member_id: int, loan: CreateLoan, session: Session = Depends(get_session)):
    db_member = session.get(Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    new_loan = Loan.model_validate(loan, update={"member_id": member_id})
    try:
        session.add(new_loan)
        session.commit()
        session.refresh(new_loan)
        return new_loan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) #to be corrected after tests to logging