from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class UserCreate(BaseModel):
    userId: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1)
    @field_validator("password")
    @classmethod
    def validate_password_length(cls, password: str):
        if len(password.encode("utf-8")) > 72: raise ValueError("Password cannot be longer than 72 bytes")
        return password

class ProfileSelect(BaseModel):
    profile_id: int

class ProfileCreate(BaseModel):
    profile_name: str = Field(min_length=1, max_length=50)
    profile_pic: str | None = Field(default=None, max_length=100)

class ProfileUpdate(BaseModel):
    profile_name: str | None = Field(default=None, min_length=1, max_length=50)
    profile_pic: str | None = Field(default=None, max_length=100)
    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if self.profile_name is None and self.profile_pic is None: raise ValueError("Provide profile_name or profile_pic")
        return self
