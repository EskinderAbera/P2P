from fastapi import FastAPI
from user.views import user_router
from internaluser.views import int_user
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


app.include_router(user_router)
app.include_router(int_user)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=7000, reload=True)