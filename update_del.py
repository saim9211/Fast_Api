from pathlib import Path
from typing import Annotated, Literal,Optional
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field

app = FastAPI()


DATA_FILE = Path(__file__).with_name("patient_without_bmi.json")


class Patient(BaseModel):
    patient_id: Annotated[str, Field(..., description="will be unique")]
    age: Annotated[int, Field(..., ge=18, lt=88, description="Will not be under_age")]
    gender: Annotated[str, Literal["male", "female", "other"]]
    systolic_bp: int
    diastolic_bp: int
    cholesterol_tier: Literal["normal", "not_normal"]
    smoker_status: str
    weight: Annotated[int, Field(..., description="enter the weight in kg")]
    height: Annotated[int, Field(..., description="enter the height in cm")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / ((self.height / 100) ** 2), 2)

    @computed_field
    @property
    def bmi_status(self) -> str:
        if self.bmi < 18.5:
            return "under_weight"
        if self.bmi < 25:
            return "normal_weight"
        if self.bmi < 35:
            return "over_weight"
        return "obese"
class UpdatePatient(BaseModel):
    age: Annotated[Optional[int], Field(default=None, description="Will not be under_age")] = None
    gender: Annotated[Optional[str], Literal["male", "female", "other"]] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    cholesterol_tier: Optional[Literal["normal", "not_normal"]] = None
    smoker_status: Optional[str] = None
    weight: Annotated[Optional[int], Field(default=None, description="enter the weight in kg")] = None
    height: Annotated[Optional[int], Field(default=None, description="enter the height in cm")] = None


def read_json_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data_to_json_file(file_path: Path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


patient_data = read_json_file(DATA_FILE)

# Retrieve patient data with sorting

@app.get("/patient")
def patient(sort_by: str = "patient_id", order: str = "asc"):
    """
    Get patient data with sorting.

    Parameters:
    - sort_by: Field to sort by (patient_id, age, systolic_bp, diastolic_bp, cholesterol_tier)
    - order: Sort order (asc or desc)
    """
    data = patient_data.copy()

    valid_fields = [
        "patient_id",
        "age",
        "systolic_bp",
        "diastolic_bp",
        "cholesterol_tier",
        "smoker_status",
        "gender",
    ]
    if sort_by not in valid_fields:
        return {"error": f"Invalid sort_by field. Valid fields are: {valid_fields}"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order. Use 'asc' or 'desc'"}

    reverse = order == "desc"
    return sorted(data, key=lambda x: x[sort_by], reverse=reverse)


@app.get("/contact")
def contact():
    return patient_data


@app.get("/about")
def about():
    return {"message": "patient about section"}

# create patient data


@app.post("/creat")
def creat_patient(patient: Patient):
    if any(existing["patient_id"] == patient.patient_id for existing in patient_data):
        raise ValueError("Patient already exists")

    patient_data.append(patient.model_dump())
    save_data_to_json_file(DATA_FILE, patient_data)
    return {"message": "Patient created successfully"}

# update patient data


# this is the code for the simple where the user can update the patient data by providing the patient_id and the updated data.
#  The updated data is optional and only the fields that are provided will be updated. 
# The updated data is validated using the UpdatePatient model. If the patient_id is not found, an error message is returned.
# if any calculationd dependent on update data so for that we have to make some changes 



# @app.put("/update/{patient_id}")
#def update_patient(patient_id: str, updated_data: UpdatePatient):
    #    for patient in patient_data:
#        if patient["patient_id"] == patient_id:
#            updated_fields = updated_data.model_dump(exclude_unset=True)
#            patient.update(updated_fields)
#            save_data_to_json_file(DATA_FILE, patient_data)
#           return {"message": "Patient updated successfully"}
#    return {"error": "Patient not found"}


# for the calculation dependent on the updated data we can use the following code to update the bmi and bmi_status fields after updating the patient data.


@app.put("/updated/{patient_id}")
def update_patient(patient_id: str, updated_data: UpdatePatient):
    for patient in patient_data:
        if patient["patient_id"] == patient_id:
            
            # 1. Merge the existing dictionary with the new incoming updates
            new_fields = updated_data.model_dump(exclude_unset=True)
            merged_dict = {**patient, **new_fields}
            
            # 2. Run it through the Pydantic model so computed fields calculate correctly
            full_patient_model = Patient(**merged_dict)
            
            # 3. Save the freshly calculated data back into your list
            patient.update(full_patient_model.model_dump())
            
            # 4. Save to file and exit
            save_data_to_json_file(DATA_FILE, patient_data)
            return {"message": "Patient updated successfully"}
            
    # If the loop finishes without a match, throw the 404
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    for patient in patient_data:
        if patient["patient_id"] == patient_id:
            patient_data.remove(patient)
            save_data_to_json_file(DATA_FILE, patient_data)
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")