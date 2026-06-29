from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Patient(BaseModel):
    name: str
    age: int
    number: Optional[int] = None
    married: bool = False
    allergy: Optional[List[str]] = None
    contact: Optional[Dict[str, Any]] = None

def insert_data(name: str, age: int):
    print(name, age)
    return {"name": name, "age": age}

def update_data(name: str, age: int, married: bool, allergy: Optional[List[str]], contact: Optional[Dict[str, Any]], number: Optional[int]):
    print(name, age, married, allergy, contact, number)
    return {"name": name, "age": age, "married": married, "allergy": allergy, "contact": contact, "number": number}

patient2 = {'name': 'paisa', 'age': 34, 'married': True, 'number': 1234567890, 'contact': {'phone': 1234567890}}

patient1=Patient(**patient2)

# insert_data(patient1.name, patient1.age)

#patient1.name='saim'
#patient1.age=25

update_data(patient1.name, patient1.age, patient1.married, patient1.allergy, patient1.contact, patient1.number)



