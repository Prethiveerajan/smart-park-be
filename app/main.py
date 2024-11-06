from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as parking_router
from app.db import get_db_connection
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Check MongoDB connection on startup
    get_db_connection()

@app.get("/")
async def root():
    return {"message": "FastAPI is working!"}
app.include_router(parking_router, prefix="/api")
