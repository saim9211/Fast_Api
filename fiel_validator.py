from pydantic import BaseModel, Field,field_validator

class Patient(BaseModel):
    name: str
    age: int
    email: str
    linkdin: str
    number: int
    married: bool
    allergy: list = []
    contact: dict = {}

    @field_validator('age')    
    @classmethod
    def validate_age(cls, value):
        if value < 1:
            raise ValueError('Age must be a positive integer')
        return value

def insert_data(name: str, age: int):
    print(name, age)
    return {"name": name, "age": age}

def update_data(name: str, age: int, email: str, linkdin: str, married: bool, allergy: list, contact: dict, number: int):
    print(name, age, email, linkdin, married, allergy, contact, number)
    return {"name": name, "age": age, "email": email, "linkdin": linkdin, "married": married, "allergy": allergy, "contact": contact, "number": number}

patient2 = {'name': 'paisa', 'age': 34, 'email': 'saimayan@gmail.com', 'linkdin': 'https://gem.com', 'married': True, 'number': 1234567890, 'contact': {'phone': 1234567890}}

patient1 = Patient(**patient2)

# insert_data(patient1.name, patient1.age)

#patient1.name='saim'
#patient1.age=25

update_data(patient1.name, patient1.age, patient1.email, patient1.linkdin, patient1.married, patient1.allergy, patient1.contact, patient1.number)



