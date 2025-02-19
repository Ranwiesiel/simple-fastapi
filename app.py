from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlmodel import Field, SQLModel, create_engine, select, Session

# sqlite database connection using sqlmodel
sqlite_file = "user.db"
sqlite_url = f"sqlite:///{sqlite_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


# user validation schema
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nama: str = Field(index=True)
    umur: int | None = Field(default=None, index=True)
    alamat: str | None = Field(default=None)
    

# init fastapi
app = FastAPI(
    title="Simple FastAPI",
    description="Simple REST API with GET, POST, and DELETE operations documentations"
)

# get data
@app.get("/api/users", status_code=200, tags=["users"],
        responses={
            200: {
                "description": "Sukses",
                "content": {
                    "application/json": {
                        "example": { 
                            "status": 200,
                            "message": "Success",
                            "data": [
                                {
                                    "id": 1,
                                    "nama": "Ronggo Widjoyo",
                                    "umur": 20,
                                    "alamat": "Lamongan"
                                },
                                {
                                    "id": 2,
                                    "nama": "Ronggo Widjoyo",
                                    "umur": 20,
                                    "alamat": "Lamongan"
                                },
                            ]
                        },
                    }
                }
            },
            404: {
                "description": "Tidak ditemukan",
                "content": {
                    "application/json": {
                        "example": {
                            "status": 404,
                            "detail": "Tidak ada data"
                        }
                    }
                }
            }
        }
)
def get_data(session: SessionDep):
    """
    Menampilkan semua data User dalam database
    """
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Tidak ada data")
    return {
        "status": 200,
        "message": "Success",
        "data": [user.model_dump() for user in users]
    }

# insert data
@app.post("/api/user", status_code=201, tags=["users"],
          responses={
              201: {
                  "description": "Berhasil membuat user",
                  "content": {
                      "application/json": {
                          "example": {
                              "status": 201,
                              "message": "User berhasil dibuat",
                              "data": {
                                  "id": 1,
                                  "nama": "Ronggo Widjoyo",
                                  "umur": 20,
                                  "alamat": "Lamongan"
                              }
                          }
                      }
                  }
              },
              400: {
                  "description": "Bad Request",
                  "content": {
                      "application/json": {
                          "example": {
                              "status": 400,
                              "detail": "Coba dengan id berbeda"
                          }
                      }
                  }
              }
          }
          )
def create_user(id: int, nama: str, umur: int, alamat: str, session: SessionDep, user: Annotated[User, Body(examples=[{"id": 1, "nama": "Ronggo Widjoyo", "umur": 20, "alamat": "Lamongan"}])]):
    """
    Mambahkan data user ke dalam database
    """
    try:
        user = User(id=id, nama=nama, umur=umur, alamat=alamat)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": 201, "message": "User berhasil dibuat", "data": user.model_dump()}
    except:
        raise HTTPException(status_code=400, detail="Coba dengan id berbeda")

# delete data
@app.delete("/api/user/{user_id}", status_code=200, tags=["users"],
            responses={
                200: {
                    "description": "Berhasil menghapus user",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": 200,
                                "message": "Data berhasil dihapus"
                            }
                        }
                    }
                },
                404: {
                    "description": "User tidak ditemukan",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": 404,
                                "detail": "User tidak ditemukan"
                            }
                        }
                    }
                }
            })
def delete_user(user_id: int, session: SessionDep, user: Annotated[User, Body(examples=[{"id": 1}])]):
    """
    Menghapus data user berdasarkan id dalam database
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    session.delete(user)
    session.commit()
    return {"status": 200, "message": "Data berhasil dihapus"}



if __name__ == '__main__':
    uvicorn.run(app, port=8000)