from fastapi import FastAPI,Path,HTTPException
import json
app=FastAPI()
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
patient_data = read_json_file('patient.json')
@app.get("/patient/{patient_id}")
def patient(patient_id: str,path: str = Path(..., description="The ID of the patient to retrieve on bases of id")):
    """
    Get patient data by patient_id.
    
    Parameters:
    - patient_id: The ID of the patient to retrieve.
    """
    # Find the patient with the given patient_id
    for patient in patient_data:
        if patient["patient_id"] == patient_id:
            return patient
    
    raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    
@app.get("/contact")
def contact():
    return patient_data
@app.get("/about")
def about():
    return {"message": "patient about section"}
