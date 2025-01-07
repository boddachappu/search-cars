from sqlmodel import Session, select
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from db import get_session
from schemas import UserOutput, User

router = APIRouter(prefix='/auth')

security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security),
                     session: Session = Depends(get_session)) -> UserOutput:
    query = select(User).where(credentials.username == User.username)
    user = session.exec(query).first()
    if user and User.verify_password(user.password, credentials.password):
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User doesn't exists")
