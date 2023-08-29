from pydantic import BaseModel, Field


class RequestPostPetWithoutPhoto(BaseModel):
    auth_key: dict = Field(...)
    name: str = Field(...)
    animal_type: str = Field(...)
    age: int = Field(...)


class ResponsePostPetWithoutPhoto(BaseModel):
    age: int = Field(...)
    animal_type: str = Field(...)
    created_at: str = Field(...)
    id: str = Field(...)
    name: str = Field(...)
    pet_photo: str = Field(...)
    user_id: str = Field(...)


class RequestGetAllPets(BaseModel):
    auth_key: dict = Field(...)
    filter: str = Field(None)
