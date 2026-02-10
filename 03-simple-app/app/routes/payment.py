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
    
    paid_amount = sum(p.amount for p in db_loan.payments)
    remaining_balance = db_loan.amount - paid_amount
    if remaining_balance < payment.amount:
        raise HTTPException(status_code=422, 
                            detail=f"remaining amount is {remaining_balance}.You are paying more.")
    
    new_payment = Payments.model_validate(payment, update={"loan_id":loan_id})
    session.add(new_payment)
    
    if (paid_amount + payment.amount) == db_loan.amount:
        db_loan.status = "paid"
        session.add(db_loan)
    
    try:
        session.commit()
        session.refresh(new_payment)
        return new_payment
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))