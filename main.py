from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import logging
from fastapi.responses import JSONResponse

# Setting buat konek database
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:''@localhost:3306/perpustakaan"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BukuModel(Base):
    __tablename__ = 'buku'
    id = Column(Integer, primary_key=True, index=True)
    judul = Column(String(255), index=True)
    penulis = Column(String(255), index=True)
    penerbit = Column(String(255), index=True)
    tahun_terbit = Column(Integer)
    konten = Column(Text)
    iktisar = Column(Text)

Base.metadata.create_all(bind=engine)

class Buku(BaseModel):
    id: int
    judul: str
    penulis: str
    penerbit: str
    tahun_terbit: int
    konten: str
    iktisar: str

    class Config:
        orm_mode = True
        
    def read(self, halaman: int):
        konten_per_halaman = self.konten.split('\n')
        for i in range(min(halaman, len(konten_per_halaman))):
            print(konten_per_halaman[i])
    
    def __str__(self):
        return f"{self.judul} by {self.penulis}"

class BukuCreate(BaseModel):
    judul: str
    penulis: str
    penerbit: str
    tahun_terbit: int
    konten: str
    iktisar: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_buku(db: Session, buku_id: int):
    return db.query(BukuModel).filter(BukuModel.id == buku_id).first()

def create_buku(db: Session, buku: BukuCreate):
    db_buku = BukuModel(**buku.dict())
    db.add(db_buku)
    db.commit()
    db.refresh(db_buku)
    return db_buku

# Creating the FastAPI app
app = FastAPI()

@app.post("/buku/", response_model=Buku)
def create_buku_endpoint(buku: BukuCreate, db: Session = Depends(get_db)):
    return create_buku(db=db, buku=buku)

@app.get("/buku/{buku_id}", response_model=Buku)
def read_buku_endpoint(buku_id: int, db: Session = Depends(get_db)):
    db_buku = get_buku(db, buku_id=buku_id)
    if db_buku is None:
        raise HTTPException(status_code=404, detail="Buku not found")
    return db_buku

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
