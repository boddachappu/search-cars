from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from schemas import Car, CarOutput, CarInput, Trip, TripsInput, User
from routers.auth import get_current_user


router = APIRouter(prefix='/api/cars')


@router.get('/')
def get_cars(size: str | None = None, doors: int | None = None, session: Session = Depends(get_session)):
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return session.exec(query).all()


@router.get('/{idx}')
def get_car_by_id(idx: int,  session: Session = Depends(get_session)) -> CarOutput:
    car = session.get(Car, idx)
    if car:
        return car
    raise HTTPException(status_code=404, detail=f"car not found with id {idx}")


@router.post('/', response_model=Car, status_code=201)
def add_cars(car: CarInput,  session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> Car:
    new_car = Car.from_orm(car)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@router.delete('/{idx}', status_code=204)
def remove_car(idx: int, session: Session = Depends(get_session)):
    car = session.get(Car, idx)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"car not found with id {idx}")


@router.put('/{idx}', response_model=Car, status_code=201)
def change_car(idx: int, new_data: CarInput, session: Session = Depends(get_session)) -> Car:
    old_car = session.get(Car, idx)
    if old_car:
        old_car.doors = new_data.doors
        old_car.size = new_data.size
        old_car.transmission = new_data.transmission
        old_car.fuel = new_data.fuel
        session.commit()
        return old_car
    else:
        raise HTTPException(status_code=404, detail=f"car not found with id {idx}")


@router.post('/{car_id}/add_trips/', response_model=Trip, status_code=201)
def add_trips(car_id: int, trips_data: TripsInput, session: Session = Depends(get_session)) -> Trip:
    old_car = session.get(Car, car_id)
    if old_car:
        new_trip = Trip.from_orm(trips_data, update={"car_id": car_id})
        old_car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"car not found with id {car_id}")