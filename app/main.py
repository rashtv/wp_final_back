from fastapi import FastAPI

from app.api.endpoints import (
    users,
    bank_accounts,
    loans,
    categories,
    subcategories,
    bonuses,
    payments,
    transactions
)
from app.database import Base, engine

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(bank_accounts.router, prefix="/accounts", tags=["bank_accounts"])
app.include_router(loans.router, prefix="/loans", tags=["loans"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(subcategories.router, prefix="/subcategories", tags=["subcategories"])
app.include_router(bonuses.router, prefix="/bonuses", tags=["bonuses"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

Base.metadata.create_all(engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
