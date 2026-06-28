from fastapi import FastAPI
import json
app=FastAPI()
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
patient_data = read_json_file('patient.json')
@app.get("/patient")
def patient(sort_by: str = "patient_id", order: str = "asc"):
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
        return {"error": f"Invalid sort_by field. Valid fields are: {valid_fields}"}
    
    # Validate order parameter
    if order not in ["asc", "desc"]:
        return {"error": "Invalid order. Use 'asc' or 'desc'"}
    
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
