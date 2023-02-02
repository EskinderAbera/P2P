from fastapi import FastAPI
from endpoints.customer import customer_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(customer_router)
# app.include_router(int_user)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)