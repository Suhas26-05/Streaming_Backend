from pydantic import BaseModel, Field, model_validator, field_validator


class UserCreate(BaseModel):

    userId: str = Field(min_length=1, max_length=50)
    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1)


    @field_validator("password")
    @classmethod
    def validate_password_length(cls, password: str):

        if len(password.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")

        return password


class UserLogin(BaseModel):

    userId: str | None = None
    email: str | None = None
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
            raise ValueError("Either username or email is required")

        if self.userId is not None and self.email is not None:
            raise ValueError("Provide either username or email, not both")

        return self