from fastapi import FastAPI

from api.routes import router as airline_router

app = FastAPI(title="Airline Seat Booking System")

app.include_router(airline_router)


@app.get("/")
def home():
    return {"message": "Airline Booking System Running"}
