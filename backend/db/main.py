from routers import Treasury_Direct
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5500",
    "https://your-frontend-domain.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the allowed origins
    allow_credentials=True, # Allow cookies to be included in cross-origin requests
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allow all headers in cross-origin requests
)


app.include_router(Treasury_Direct.router)

