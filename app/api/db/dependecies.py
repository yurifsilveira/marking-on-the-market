from typing import Annotated
from sqlmodel import Session
from fastapi import Depends

from . import config

SessionDep = Annotated[Session, Depends(config.get_session)]