from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

patient_data = read_json_file('patient.json')

@app.get("/patient/{patient_id}")
def get_patient_by_id(patient_id: str = Path(..., description="The ID of the patient to retrieve")):
    """
    Get patient data by patient_id.
    
    Parameters:
    - patient_id: The ID of the patient to retrieve.
    """
    for patient in patient_data:
        if patient["patient_id"] == patient_id:
            return patient
    
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")

@app.get("/patient")
def get_all_patients(
    sort_by: str = Query("patient_id", description="Field to sort by"),
    order: str = Query("asc", description="Sort order (asc or desc)")
):
    """
    Get patient data with sorting.
    
    Parameters:
    - sort_by: Field to sort by (patient_id, age, systolic_bp, diastolic_bp, body_mass_index, cholesterol_tier)
    - order: Sort order (asc or desc)
    """
    data = patient_data.copy()
    
    # Validate sort_by parameter
    valid_fields = ["patient_id", "age", "systolic_bp", "diastolic_bp", "body_mass_index", "cholesterol_tier", "smoker_status", "gender"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Valid fields are: {valid_fields}")
    
    # Validate order parameter
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'")
    
    # Sort the data
    reverse = True if order == "desc" else False
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=reverse)
    
    return sorted_data

@app.get("/contact")
def contact():
    return patient_data

@app.get("/about")
def about():
    return {"message": "patient about section"}
