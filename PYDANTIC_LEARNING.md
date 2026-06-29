# Pydantic Learning Guide

## What is Pydantic?
Pydantic is a Python library for data validation and settings management using Python type annotations. It enforces type hints at runtime and provides user-friendly error messages.

---

## 1. BaseModel - Foundation of Pydantic

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    email: str
```

**Key Points:**
- Every Pydantic model inherits from `BaseModel`
- Type hints are mandatory and enforced
- Pydantic validates data types automatically
- Invalid data raises `ValidationError`

---

## 2. Creating Instances

### Direct instantiation:
```python
patient = Patient(name="John", age=30, email="john@example.com")
```

### From dictionary (unpacking):
```python
data = {'name': 'John', 'age': 30, 'email': 'john@example.com'}
patient = Patient(**data)
```

---

## 3. Type Hints & Field Types

### Basic Types:
```python
class Example(BaseModel):
    name: str          # String
    age: int           # Integer
    active: bool       # Boolean
    tags: list         # List
    metadata: dict     # Dictionary
```

### Advanced Types:
```python
from typing import Optional, List, Dict, Any

class Advanced(BaseModel):
    email: Optional[str] = None          # Optional field with default
    hobbies: List[str] = []              # List of strings
    contact: Dict[str, Any] = {}         # Dictionary
    alternate_age: Optional[int] = None  # Optional integer
```

---

## 4. Default Values

```python
class Patient(BaseModel):
    name: str
    age: int
    married: bool = False              # Default False
    allergies: list = []               # Default empty list
    contact: dict = {}                 # Default empty dict
```

**Important:** Mutable defaults (list, dict) should have default values to avoid issues.

---

## 5. Field Validator - Validate Individual Fields

Used to validate a single field with custom logic.

```python
from pydantic import field_validator

class Patient(BaseModel):
    age: int
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, value):
        if value < 0:
            raise ValueError('Age must be a positive integer')
        return value
```

**Key Points:**
- Placed INSIDE the class
- Uses `@classmethod` decorator
- Can raise `ValueError` for invalid data
- Receives the field value

---

## 6. Model Validator - Validate Multiple Fields

Used to validate relationships between multiple fields.

```python
from pydantic import model_validator

class Patient(BaseModel):
    age: int
    contact: dict
    
    @model_validator(mode='before')
    @classmethod
    def validate_patient(cls, model):
        # mode='before': input is a dictionary
        if model['age'] < 1 and 'emergency' not in model['contact']:
            raise ValueError('Age must be positive and emergency contact required')
        return model
```

**Key Points:**
- `mode='before'`: Validates raw input (dict)
- `mode='after'`: Validates after individual fields are validated
- With `mode='before'`, access fields as dict: `model['field_name']`
- With `mode='after'`, access as object: `model.field_name`

---

## 7. Computed Fields - Calculate Properties

Used to create read-only calculated properties.

```python
from pydantic import computed_field

class Patient(BaseModel):
    age: int
    
    @computed_field
    @property
    def age_in_months(self) -> int:
        return self.age * 12
```

**Key Points:**
- Uses `@computed_field` and `@property`
- NOT `@classmethod` (it's an instance property)
- Automatically calculated when accessing the field
- Included in model output when serialized

**Usage:**
```python
patient = Patient(age=25)
print(patient.age_in_months)  # Output: 300
```

---

## 8. Email & URL Validation

```python
from pydantic import EmailStr, AnyUrl

class Contact(BaseModel):
    email: EmailStr           # Validates email format
    website: AnyUrl           # Validates URL format
```

**Requirements:**
```bash
pip install pydantic[email]
```

**Note:** You can skip these if not needed and use basic `str` instead.

---

## 9. Serialization - Converting to JSON/Dict

```python
patient = Patient(name="John", age=30, email="john@example.com")

# To dictionary
patient_dict = patient.model_dump()
# Output: {'name': 'John', 'age': 30, 'email': 'john@example.com'}

# To JSON string
patient_json = patient.model_dump_json()
# Output: '{"name":"John","age":30,"email":"john@example.com"}'
```

---

## 10. Error Handling

```python
from pydantic import ValidationError

try:
    patient = Patient(name="John", age="thirty")  # Wrong type
except ValidationError as e:
    print(e.errors())
    # Shows detailed error info including field, type, and reason
```

---

## 11. Common Mistakes & Solutions

### ❌ Mistake 1: Validator outside the class
```python
# WRONG
class Patient(BaseModel):
    age: int

@field_validator('age')  # ❌ Outside class
def validate_age(cls, v):
    return v
```

### ✅ Solution: Place inside the class
```python
# CORRECT
class Patient(BaseModel):
    age: int
    
    @field_validator('age')  # ✅ Inside class
    @classmethod
    def validate_age(cls, v):
        return v
```

---

### ❌ Mistake 2: Wrong decorator for computed field
```python
# WRONG
@computed_field
@classmethod  # ❌ Wrong
def calculated(cls) -> int:
    return 100
```

### ✅ Solution: Use @property
```python
# CORRECT
@computed_field
@property  # ✅ Correct
def calculated(self) -> int:
    return 100
```

---

### ❌ Mistake 3: Optional without default
```python
# WRONG
class Patient(BaseModel):
    email: Optional[str]  # ❌ No default value
```

### ✅ Solution: Add default value
```python
# CORRECT
class Patient(BaseModel):
    email: Optional[str] = None  # ✅ Has default
```

---

### ❌ Mistake 4: Missing `@classmethod` in validators
```python
# WRONG
@field_validator('age')
def validate_age(self, v):  # ❌ Missing @classmethod
    return v
```

### ✅ Solution: Add @classmethod
```python
# CORRECT
@field_validator('age')
@classmethod  # ✅ Added
def validate_age(cls, v):
    return v
```

---

## 12. FastAPI Integration

Pydantic models work perfectly with FastAPI for request/response validation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.post("/items/")
def create_item(item: Item):
    return item
```

FastAPI automatically:
- Validates request data against the model
- Returns 422 error for invalid data
- Generates API documentation
- Converts response to JSON

---

## 13. Best Practices

✅ **DO:**
- Use type hints for all fields
- Provide default values for optional fields
- Place validators inside the model class
- Use `@classmethod` for field/model validators
- Use `@property` for computed fields
- Validate related fields together with `@model_validator`

❌ **DON'T:**
- Put validators outside the class
- Mix `@classmethod` with `@property`
- Use mutable defaults without default values
- Forget `@classmethod` in validators
- Return wrong types from validators

---

## Summary of Decorators

| Decorator | Purpose | Location | Notes |
|-----------|---------|----------|-------|
| `@field_validator` | Validate single field | Inside class | Needs `@classmethod` |
| `@model_validator` | Validate multiple fields | Inside class | Needs `@classmethod` |
| `@computed_field` | Calculate read-only property | Inside class | Needs `@property` |

---

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [FastAPI + Pydantic](https://fastapi.tiangolo.com/)
- [Type Hints in Python](https://docs.python.org/3/library/typing.html)

---

## Quick Reference

```python
from pydantic import BaseModel, field_validator, model_validator, computed_field
from typing import Optional, List, Dict, Any

class Patient(BaseModel):
    # Basic fields
    name: str
    age: int
    email: str
    
    # Optional fields with defaults
    phone: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    
    # Field validator
    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
    
    # Model validator
    @model_validator(mode='before')
    @classmethod
    def validate_model(cls, data):
        if data['age'] < 18 and 'guardian' not in data:
            raise ValueError('Guardian required for minors')
        return data
    
    # Computed field
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 18:
            return 'Minor'
        elif self.age < 65:
            return 'Adult'
        else:
            return 'Senior'

# Usage
patient = Patient(
    name='John',
    age=30,
    email='john@example.com'
)

print(patient.model_dump())
print(patient.model_dump_json())
```

---

**Congratulations!** 🎉 You now understand the core concepts of Pydantic!
