from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as json
from fastapi.security import OAuth2PasswordRequestForm
import functions.dbConnector as dbConnector
from models.users import Token, UpdatedUser, User, UserSecure, UserInDB
from services.auth import (
    get_current_active_user,
    obtain_token)

usr = APIRouter(prefix="/users",
                tags=["Route for users management"],
                responses={404: {"description": "Not found"}})


## Update user entry 
#@usr.put("", dependencies=[Depends(check_admin)])
#async def update_user(user_name: str, new_data: AdminUpdatedUser):
#    return conn_usr.update_user(original_value=user_name, new_data=json(new_data))


# Delete user entry
#@usr.delete("")
#async def delete_known_user(user_id: int):
#    return dbConnector.delete_register(id=user_id, table='Users')
#
#
#@usr.get("/get_user", response_model=User)
#async def get_user(username:str):
#    return dbConnector.get_user(username)
#


@usr.get("/me/", response_model=UserSecure, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User=Depends(get_current_active_user)):
    return current_user

# Update user entry 
#@usr.put("/me")
#async def update_my_user(updated_info: UpdatedUser, current_user: UserInDB=Depends(get_info_if_active_user)):
#    return conn_usr.update_my_user(user=json(current_user), new_data=json(updated_info))

@usr.get("/all", response_model=list[UserInDB], dependencies=[Depends(get_current_active_user)],
                 status_code=status.HTTP_200_OK)
async def get_all_users():
    return dbConnector.get_all_users()

# Insert a new user into the database                 
@usr.post("/", response_model=UserInDB, dependencies=[Depends(get_current_active_user)],
               status_code=status.HTTP_201_CREATED)
async def create_new_user(new_user: User):
    return dbConnector.create_user(json(new_user))

# Update user information
@usr.put("/{id}", response_model=UserInDB, dependencies=[Depends(get_current_active_user)],
                  status_code=status.HTTP_200_OK)
async def update_user(updated_info: UpdatedUser, user_id: int):
    return dbConnector.update_user(user_id=user_id, user_mod=json(updated_info))

# Login to get an access token                             
@usr.post("/token", response_model=Token)
async def login_for_access_token(login_data: OAuth2PasswordRequestForm=Depends()):
    return obtain_token(login_data)