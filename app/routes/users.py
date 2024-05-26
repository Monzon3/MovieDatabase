from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as json
from fastapi.security import OAuth2PasswordRequestForm
import functions.dbConnector as dbConnector
from models.users import Token, AdminUpdatedUser, UpdatedUser, User, UserSecure, UserInDB
from services.auth import (
    check_admin,
    get_current_active_user,
    obtain_token)

usr = APIRouter(prefix="/users",
                tags=["Route for users management"],
                responses={404: {"description": "Not found"}})


# Get current user information
@usr.get("/me/", response_model=UserSecure, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User=Depends(get_current_active_user)):
    return current_user

# Update current user information 
@usr.put("/me", response_model=UserSecure, status_code=status.HTTP_200_OK)
async def update_my_user(updated_info: UpdatedUser, current_user: UserInDB=Depends(get_current_active_user)):
    return dbConnector.update_user(user_id=current_user['id'], user_mod=json(updated_info))

# Get all users
@usr.get("/all", response_model=list[UserInDB], dependencies=[Depends(check_admin)],
                 status_code=status.HTTP_200_OK)
async def get_all_users():
    return dbConnector.get_all_users()

# Insert a new user into the database                 
@usr.post("/", response_model=UserInDB, dependencies=[Depends(check_admin)],
               status_code=status.HTTP_201_CREATED)
async def create_new_user(new_user: User):
    return dbConnector.create_user(json(new_user))

# Update user entry
@usr.put("/{id}", response_model=UserInDB, dependencies=[Depends(check_admin)],
                  status_code=status.HTTP_200_OK)
async def update_user(updated_info: AdminUpdatedUser, user_id: int):
    return dbConnector.update_user(user_id=user_id, user_mod=json(updated_info))

# Delete user entry
@usr.delete("/{id}", dependencies=[Depends(check_admin)], status_code=status.HTTP_200_OK)
async def delete_user(id: int):
    return dbConnector.delete_user(user_id=id)

# Login to get an access token                             
@usr.post("/token", response_model=Token)
async def login_for_access_token(login_data: OAuth2PasswordRequestForm=Depends()):
    return obtain_token(login_data)