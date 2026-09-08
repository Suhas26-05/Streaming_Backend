from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator


class UserCreate(BaseModel):
    userId: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1)

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, password: str):
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return password


class UserLogin(BaseModel):
    userId: str | None = None
    email: EmailStr | None = None
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, password: str):
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return password

    @model_validator(mode="after")
    def validate_login_method(self):
        if self.userId is None and self.email is None:
            raise ValueError("Either userId or email is required")

        if self.userId is not None and self.email is not None:
            raise ValueError("Provide either userId or email, not both")

        return self


class ProfileSelect(BaseModel):
    profile_id: int


class UserLogout(BaseModel):
    session_id: int


class ProfileCreate(BaseModel):
    profile_name: str = Field(min_length=1, max_length=50)
    profile_pic: str | None = Field(default=None, max_length=100)


class ProfileUpdate(BaseModel):
    profile_name: str | None = Field(default=None, min_length=1, max_length=50)
    profile_pic: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if self.profile_name is None and self.profile_pic is None:
            raise ValueError("Provide profile_name or profile_pic")
        return self
