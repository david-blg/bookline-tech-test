from fastapi import FastAPI



app = FastAPI(
    title="Car Rental API",
    description="A simple REST API for car rental service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/")
def root():
    return {
        "message": app.description,
        "status": "active",
        "docs": app.docs_url,
        "redoc": app.redoc_url,
    }