from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from app.controllers import setup_controller, consignment_controller, manifest_controller

# Create FastAPI app
app = FastAPI(
    title="Example Linnworks Shipping Integration",
    description="An Python example implementing a simple Shipping Integration for Linnworks. This example uses FastAPI.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from controllers
app.include_router(setup_controller.router, prefix="/api/Setup", tags=["Setup"])
app.include_router(consignment_controller.router, prefix="/api/Consignment", tags=["Consignment"])
app.include_router(manifest_controller.router, prefix="/api/Manifest", tags=["Manifest"])

@app.get("/")
async def root():
    return {"message": "Example Linnworks Shipping Integration"}

# Exception handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"isError": True, "errorMessage": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)