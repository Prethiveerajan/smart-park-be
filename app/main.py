from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as parking_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parking_router, prefix="/api")
