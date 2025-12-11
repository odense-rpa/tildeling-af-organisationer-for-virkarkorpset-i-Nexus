from pydantic import BaseModel, field_validator, RootModel
from datetime import datetime


class Vagt(BaseModel):
    vagtdato: datetime
    vikarnavn: str
    vikarId: int
    uddannselse: str
    kundenavn: str
    kundeId: int

    @field_validator('vikarnavn')
    @classmethod
    def validate_vikarnavn(cls, v):
        if not v or not v.strip():
            raise ValueError('vikarnavn must not be empty')
        return v

    @field_validator('vikarId', 'kundeId')
    @classmethod
    def validate_ids(cls, v):
        if v is None:
            raise ValueError('workerId and clientId cannot be null')
        return v
