from fastapi import FastAPI
from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session
from pydantic import BaseModel
from deta import Deta
import json

# localの場合は、project keyが必要だが、Deta base上ではいらない
deta = Deta()
users = deta.Base("fastapi-users")
rooms = deta.Base("fastapi-rooms")
bookings = deta.Base("fastapi-bookings")

app = FastAPI()

class User(BaseModel):
  name: str
  age: int
  hometown: str

class UserUpdate(BaseModel):
  name: str = None
  age: int = None
  hometown: str = None

class Room(BaseModel):
  room_name: str
  capacity: int

class Booking(BaseModel):
  user_key: str
  room_key: str
  reserved_num: int
  start_date_time: str
  end_date_time: str


@app.get("/")
def index():
  return {"message": "hello world"}

# https://docs.deta.sh/docs/base/sdk
@app.get("/users")
def read_user():
  return next(users.fetch())

@app.get("/users/{uid}")
def read_user(uid: str):
  user = users.get(uid)
  if user:
    return user
  res = JSONResponse({"message": "user not found"}, status_code=404)
  return res

@app.post("/users", status_code=200)
def create_user(user: User):
  user = users.put(user.dict())
  # return next(users.fetch())
  return json.dumps(user)

@app.patch("/users/{uid}")
def update_user(uid: str, uu:UserUpdate):
  # print(uid,uu.dict())
  update = {k:v for k,v in uu.dict().items() if v is not None}
  try:
    users.update(update, uid)
    return users.get(uid)
  except Exception:
    return JSONResponse({"message": "user not found"}, status_code=404)

@app.delete("/users/{uid}")
def delete_user(uid: str):
  # print(uid,uu.dict())
  users.delete(uid)
  return JSONResponse({"message": "user is deleted"}, status_code=200)

# if __name__ == '__main__':
#   main()

@app.get("/rooms")
def read_room():
  return next(rooms.fetch())

@app.post("/rooms", status_code=200)
def create_room(room: Room):
  room = rooms.put(room.dict())
  # return next(rooms.fetch())
  return json.dumps(room)

@app.get("/bookings")
def read_booking():
  return next(bookings.fetch())

@app.post("/bookings", status_code=200)
def create_booking(booking: Booking):
  booking = bookings.put(booking.dict())
  # return next(rooms.fetch())
  return json.dumps(booking)