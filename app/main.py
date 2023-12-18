from fastapi import FastAPI

from app.api.endpoints import users, bank_accounts
from app.database import Base, engine

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(bank_accounts.router, prefix="/accounts", tags=["bank_accounts"])

Base.metadata.create_all(engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
