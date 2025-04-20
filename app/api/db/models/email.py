from sqlmodel import Field, SQLModel, Integer

class email_log(SQLModel,table=True):
        
    id : str = Field(default=None,primary_key=True)