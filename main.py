from fastapi import FastAPI
from endpoints.customer import customer_router
from endpoints.loan import loan_router
from endpoints.users import user_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "users",
        "description": "Operation with internal user",
    },
    {
        "name": "customers",
        "description": "Operation with customers",
    },
    {
        "name": "loans",
        "description": "Operation with loan"
    }
]

app = FastAPI(openapi_tags=tags_metadata)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(customer_router)
app.include_router(user_router)
app.include_router(loan_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)