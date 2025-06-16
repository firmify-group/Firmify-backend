from fastapi import APIRouter, Form, HTTPException


import secrets


from typing import Annotated

from ....models.request_models.user_in import UserRequest, UserSave
from ....models.response_models.user_out import UseOutData, UserAuthOut
from ....models.response_models.token import JWTToken
from ....service import auth_service
from ....database import user_database as user_db

router = APIRouter()


from ....database.deps import super_client



@router.post("/login")
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    if not email or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    
    
    try:
        response = super_client.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
        )
        if response.session is None:
            raise HTTPException(status_code=401, detail="Invalid credentials or user not found.")
    except Exception as e:
        print("Error during login:", e)
        raise HTTPException(status_code=401, detail="Invalid credentials or user not found.")
    
   
    token = JWTToken(
                    id=  super_client.auth.get_session().user.id,
                    rol = user_db.get_rol(email=email),
                )
    response  = UserAuthOut(
        status= True,
        data= UseOutData
        (
            token= auth_service.createToken
            (
                token
            ),
            expires_in = 3600,
            token_type = "Bearer"
        ),
        message= "Acceso aprobado",
    )
     
    
    return response


@router.post("/register")
async def register(
    user: Annotated[UserRequest, Form()],
    
):
    """ 
    La contraseña se genera aleatoriamente, en la base de datos se guarda encriptada.
    """

    if not user.email or not user.full_name or not user.rut :
        raise HTTPException(status_code=400, detail="All fields are required.")
    
    hex_password = secrets.token_hex(4)  # 4 bytes = 8 hex digits
    hex_signature = secrets.token_hex(4)
    
    


    print("hex_password", hex_password)
    
    newUser = auth_service.create_employee(
        UserSave(
        full_name=user.full_name,
        rut=user.rut,
        email=user.email,
        password= hex_password,  
        signature= hex_signature  # Placeholder for signature
    ))
    return {"message": "Registration successful", "user": newUser}



@router.get("/test")
async def test():
    """
    Test endpoint to verify the router is working.
    
    """
   
   
    """
    response = super_client.auth.sign_in_with_password(
    {
        "email": "datito12345@gmail.com",
        "password": "test_password",
    }
    )
    print(response)
    print("user token:", response.session.access_token, "token type:", response.session.token_type)
    print("-------------------------------------")
    print("sesion", super_client.auth.get_session())
    """

    data = [{},{}]
    response = super_client.table("request").select("*").execute().data

    print("Response from request table:", response)

    data[0] = response
    
    sesion = super_client.auth.get_session()
    print("Session data:", sesion)
    
    #data[1] = sesion
    
    return {"message": "Test successful", "data": data}


@router.post("/logout")
async def logout():
    """
    Endpoint to log out the user.
    
    This will clear the session and invalidate the token.
    """
    try:
        super_client.auth.sign_out()
        return {"message": "Logout successful"}
    except Exception as e:
        print("Error during logout:", e)
        raise HTTPException(status_code=500, detail="Logout failed")


