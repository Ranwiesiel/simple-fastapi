from typing import Annotated, List

from fastapi import HTTPException, Body, APIRouter
from sqlmodel import select

from connection import SessionDep
from schemas import User


user_router = APIRouter()

# get all users
@user_router.get("/", status_code=200, response_model=List[User],
        responses={
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
def get_all_users(session: SessionDep):
    """
    Menampilkan semua data User dalam database
    """
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Tidak ada data")
    return users

# get user
@user_router.get("/{user_id}", status_code=200, response_model=User,
                 responses={
                        404: {
                            "description": "User tidak ditemukan",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "status": 404,
                                        "detail": "User tidak ada"
                                    }
                                }
                            }
                        }
                    }
                 )
def get_user(user_id: int, session: SessionDep):
    """
    Mengambil data user berdasarkan *id* user
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ada")
    return user.model_dump()

# insert data
@user_router.post("/", status_code=201,
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
def create_user(user: Annotated[User, Body(examples=[{"id": 1, "nama": "Ronggo Widjoyo", "umur": 20, "alamat": "Lamongan"}])], session: SessionDep):
    """
    Mambahkan data user ke dalam database
    """
    user_sekarang = session.get(User, user.id)
    if user_sekarang:
        raise HTTPException(status_code=400, detail="Coba dengan id berbeda")
    
    try:
        session.add(user)
        session.flush()
        session.commit()
        session.refresh(user)
        return {"status": 201, "message": "User berhasil dibuat", "data": user.model_dump()}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal membuat user: {str(e)}")

# delete data
@user_router.delete("/{user_id}", status_code=200,
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
def delete_user(user_id: int, session: SessionDep):
    """
    Menghapus data user berdasarkan id dalam database
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    try:
        session.delete(user)
        session.commit()
        return {"status": 200, "message": "Data berhasil dihapus"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal menghapus user: {str(e)}")