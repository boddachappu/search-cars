from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


class TripsInput(SQLModel):
    start: int
    end: int
    description: str

    model_config = {
        'json_schema_extra': {
            'example': {
                'start': 0,
                'end': 10,
                'description': 'dinner'
            }
        }
    }


class TripsOutput(TripsInput):
    id: int


class Trip(TripsInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    model_config = {
        "json_schema_extra": {
            "example":
                {
                    "size": "m",
                    "fuel": "petrol",
                    "doors": 4,
                    "transmission": "manual"
                }
        }
    }


class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")


class CarOutput(CarInput):
    id: int
    trips: list[TripsOutput] = []


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, index=True, unique=True))
    password_hash: str = " "

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class UserOutput(CarInput):
    id: int
    username: str


