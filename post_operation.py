from pathlib import Path
from typing import Annotated, Literal
import json

from fastapi import FastAPI
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
        return round(self.weight / (self.height ** 2), 2)

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


def read_json_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data_to_json_file(file_path: Path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


patient_data = read_json_file(DATA_FILE)


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


@app.post("/creat")
def creat_patient(patient: Patient):
    if any(existing["patient_id"] == patient.patient_id for existing in patient_data):
        raise ValueError("Patient already exists")

    patient_data.append(patient.model_dump())
    save_data_to_json_file(DATA_FILE, patient_data)
    return {"message": "Patient created successfully"}


