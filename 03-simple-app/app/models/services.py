from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from app.dependancies import utcnow

#==================================== Member models ============================================
# 1. THE TRUNK: Only the absolute common fields
class MemberBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    date_of_birth: date = Field() 
    gender: str = Field()
    phone_number: str = Field(max_length=15, index=True) 

# 2. THE INPUT: For creating a member
class MemberCreate(MemberBase):
    pass 

# 3. THE UPDATE: For PATCH requests
class MemberUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None

# 4. THE DATABASE: The actual table
class Member(MemberBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(
        default_factory=utcnow, 
        sa_column_kwargs={"onupdate": utcnow}
    )
    loans: List["Loan"] = Relationship(back_populates="member")

# 5. THE OUTPUT: What the API returns to the user
class MemberPublic(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
class MemberAndLoan(MemberPublic):
    loans: List["PublicLoan"] = []
#============================= Loan models======================================================

class BaseLoan(SQLModel):
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    payable_at: date = Field()

class Loan(BaseLoan, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    approved_at: datetime = Field(default_factory=utcnow)
    member_id: int = Field(foreign_key="member.id", ondelete="CASCADE")
    member: Optional[Member] = Relationship(back_populates="loans")
    payments: List["Payments"] = Relationship(back_populates="loan", cascade_delete=True)
    
class CreateLoan(BaseLoan):
    pass

class UpdateLoan(SQLModel):
    amount: Optional[Decimal] = Field(max_digits=12, decimal_places=2)
    approved_at: Optional[datetime] = Field(default_factory=utcnow)
    payable_at: Optional[date] = Field()

class PublicLoan(BaseLoan):
    id: int
    member_id: int
    
#======================== payments models ==================================================

class BasePayments(SQLModel):
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    paid_at: datetime = Field(default_factory=utcnow)

class Payments(BasePayments, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loan_id: int = Field(foreign_key="loan.id", ondelete="CASCADE")
    loan: Optional[Loan] = Relationship(back_populates="payments")
    
class CreatePayments(BasePayments):
    pass

class UpdatePayments(SQLModel):
    amount: Optional[Decimal] = Field(max_digits=12, decimal_places=2)
    paid_at: Optional[datetime] = Field(default_factory=utcnow)
    
class PublicPayments(BasePayments):
    id: Optional[int] = Field(default=None, primary_key=True)