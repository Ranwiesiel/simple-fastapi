from sqlmodel import Field, SQLModel


# user validation schema
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nama: str = Field(index=True)
    umur: int = Field(default=None)
    alamat: str = Field(default=None)

    class Config:
        from_attributes = True  # Agar FastAPI bisa mengonversi objek SQLModel ke JSON