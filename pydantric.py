from pydantic import BaseModel
class Patient(BaseModel):
    name: str
    age: int

def insert_data(name: str, age: int):
    print(name, age)
    return "inserted successfully"
def update_data(name: str, age: int):
    print(name, age)
    return "updated successfully"
patient2={'name':'paisa','age':"34"}
patient1=Patient(**patient2)

# insert_data(patient1.name, patient1.age)
patient1.name='saim'
patient1.age=25
update_data(patient1.name, patient1.age)



