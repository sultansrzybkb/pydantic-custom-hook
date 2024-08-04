from pydantic import BaseModel
#pydantic modelleri
class MyModel(BaseModel):
    name: str
    age: int=30 # Bu alan tip ipucu içerdiği için kurallara uygundur

class MyInvalidModel(BaseModel):
    name : str=  "John"
    age = 33 # Bu alan tip ipucu içermediği için hata verecektir




 
 