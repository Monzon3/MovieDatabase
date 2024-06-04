from pydantic import BaseModel, Field
from typing import Literal, Optional

# UpdatedUser is used by a user only to change its own e-mail or password
class UpdatedUser(BaseModel):
    Email: Optional[str] = Field(example="valid_email@server.com",
                       pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$",
                       default=None)
    Password: Optional[str] = Field(description="The password cannot be empty", min_length=1,
                                    default=None)

# AdminUpdatedUser allows the admin to modify the Name and RankID of the user
class AdminUpdatedUser(UpdatedUser):
    Name: Optional[str] = Field(description="The username cannot be empty",  
                          example="example_name",
                          pattern=r"[0-9A-Za-z_]", 
                          min_length=1, max_length=20, default=None)
    RankID: Literal[1, 2, 3] = None
    Disabled: Optional[bool] = False 

# UserSecure does not have the password attribute, even if it is hashed
class UserSecure(BaseModel):
    id: Optional[int] = None
    username: str = Field(description="The username cannot be empty", 
                          example="example_name",
                          pattern=r"^[0-9A-Za-z_]+$", 
                          min_length=1, max_length=20)
    email: str = Field(example="valid_email@server.com",
                       pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
    user_rank: Literal["admin", "powerUser", "user"] = "user"
    disabled: Optional[bool] = False

class User(UserSecure):
    password: str = Field(description="The password cannot be empty", 
                          pattern='^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])[a-zA-Z0-9!"·#$%&()]{8,16}$', min_length=1)


# Token-related classes
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None