from pydantic import BaseModel, EmailStr, field_validator, model_validator

class UserLogin(BaseModel):
    userId: str | None = None
    email: EmailStr | None = None
    password: str
    @field_validator("password")
    @classmethod
    def validate_password_length(cls, password: str):
        if len(password.encode("utf-8")) > 72: raise ValueError("Password cannot be longer than 72 bytes")
        return password
    @model_validator(mode="after")
    def validate_login_method(self):
        if self.userId is None and self.email is None: raise ValueError("Either userId or email is required")
        if self.userId is not None and self.email is not None: raise ValueError("Provide either userId or email, not both")
        return self

class UserLogout(BaseModel):
    session_id: int
