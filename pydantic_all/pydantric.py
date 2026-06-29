from pydantic import BaseModel, EmailStr, AnyUrl,Field
from typing import Optional, List, Dict, Any,Annotated

class Patient(BaseModel):
    name: str
    age: Annotated[int, Field(gt=18, lt=101,title='Age of the patient', description='Age must be between 18 and 100')]
    email: EmailStr = None
    linkdin: AnyUrl = None
    number: Optional[int] = None
    married: bool = False
    allergy: Optional[List[str]] = None
    contact: Optional[Dict[str, Any]] = None

def insert_data(name: str, age: int):
    print(name, age)
    return {"name": name, "age": age}

def update_data(name: str, age: int, email: EmailStr, linkdin: AnyUrl, married: bool, allergy: Optional[List[str]], contact: Optional[Dict[str, Any]], number: Optional[int]):
    print(name, age, email,linkdin,married, allergy, contact, number,)
    return {"name": name, "age": age, "email": email, "linkdin": linkdin, "married": married, "allergy": allergy, "contact": contact, "number": number}

patient2 = {'name': 'paisa', 'age': 34, 'email': 'saimayan@gmail.com', 'linkdin': 'https://gem.com', 'married': True, 'number': 1234567890, 'contact': {'phone': 1234567890}}

patient1 = Patient(**patient2)

# insert_data(patient1.name, patient1.age)

#patient1.name='saim'
#patient1.age=25

update_data(patient1.name, patient1.age, patient1.email, patient1.linkdin, patient1.married, patient1.allergy, patient1.contact, patient1.number)



