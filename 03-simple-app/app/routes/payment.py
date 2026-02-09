from sqlmodel import SQLModel, Session, select
from fastapi import APIRouter, Depends, Query, HTTPException
from app.models.services import CreatePayments, UpdatePayments, PublicPayments, Payments, Loan
from app.database import get_session

payment_router = APIRouter()

@payment_router.post('/payments/{loan_id}', response_model=PublicPayments, status_code=201)
def register_payment(loan_id: int, payment: CreatePayments, session: Session=(Depends(get_session))):
    db_loan = session.get(Loan, loan_id)
    if not db_loan:
        raise HTTPException(status_code=404,  detail="Loan not found")
    new_payment = Payments.model_validate(payment, update={"loan_id":loan_id})
    try:
        session.add(new_payment)
        session.commit()
        session.refresh(new_payment)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))