import os
import io
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

# ReportLab for generating dynamic Prescription PDFs
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# FHIR R4 Resources
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.patient import Patient
from fhir.resources.condition import Condition
from fhir.resources.documentreference import DocumentReference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding

from auth import hash_password, verify_password, create_access_token

app = FastAPI(title="MediKiosk Backend Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploaded_files"
PRESCRIPTION_DIR = "./prescriptions"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PRESCRIPTION_DIR, exist_ok=True)

sessions = {}

class PatientRegisterRequest(BaseModel):
    patient_name: str
    contact_number: str
    contact_email: str
    symptoms: str

class IssueAppointmentRequest(BaseModel):
    session_id: str
    appointment_date: str
    appointment_time: str
    doctor_notes: str
    prescription_text: str

class GenerateFHIRRequest(BaseModel):
    session_id: str
    patient_name: str
    contact_number: str
    contact_email: str
    primary_symptom: str


def build_prescription_pdf(file_path: str, patient_name: str, date_str: str, time_str: str, notes: str, rx_text: str):
    """Generates an official appointment & prescription PDF document."""
    c = canvas.Canvas(file_path, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillColorRGB(0.08, 0.58, 0.53)  # Teal
    c.drawString(50, 750, "MediKiosk Medical Center")
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(50, 735, "Official Clinical Appointment Letter & Digital Prescription")
    c.line(50, 725, 550, 725)
    
    # Patient & Schedule Info
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, 695, f"Patient Name: {patient_name}")
    
    c.setFont("Helvetica", 11)
    c.drawString(50, 675, f"Scheduled Date: {date_str} at {time_str}")
    c.drawString(50, 658, f"Issued On: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Clinical Notes
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 620, "Doctor's Assessment / Clinical Notes:")
    c.setFont("Helvetica", 10)
    
    y_pos = 600
    for line in notes.split('\n'):
        c.drawString(60, y_pos, f"• {line}")
        y_pos -= 18
        
    # Prescription Box
    y_pos -= 15
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.08, 0.58, 0.53)
    c.drawString(50, y_pos, "Rx - Immediate Medication Instructions:")
    
    y_pos -= 20
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 0)
    for line in rx_text.split('\n'):
        c.drawString(60, y_pos, f"▸ {line}")
        y_pos -= 18
        
    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, 50, "Verified by MediKiosk AI Triage System. Present this document upon arrival.")
    
    c.save()


@app.get("/")
def read_root():
    return {"message": "MediKiosk Engine Active"}


@app.post("/api/v1/intake/register")
def register_patient(req: PatientRegisterRequest):
    session_id = f"ses-{uuid.uuid4().hex[:8]}"
    sessions[session_id] = {
        "created_at": datetime.now().isoformat(),
        "patient_name": req.patient_name,
        "contact_number": req.contact_number,
        "contact_email": req.contact_email,
        "symptoms": req.symptoms,
        "documents": [],
        "appointment": None
    }
    return {"session_id": session_id, "status": "registered"}


@app.post("/api/v1/doctor/issue-appointment")
def issue_appointment(req: IssueAppointmentRequest):
    """Issues an appointment date, time, and prescription PDF for a patient."""
    if req.session_id not in sessions:
        return {"error": "Patient session not found"}
    
    patient = sessions[req.session_id]
    pdf_filename = f"Prescription_{req.session_id}.pdf"
    pdf_path = os.path.join(PRESCRIPTION_DIR, pdf_filename)
    
    # Generate the physical PDF prescription
    build_prescription_pdf(
        file_path=pdf_path,
        patient_name=patient["patient_name"],
        date_str=req.appointment_date,
        time_str=req.appointment_time,
        notes=req.doctor_notes,
        rx_text=req.prescription_text
    )
    
    download_url = f"http://127.0.0.1:8000/api/v1/prescription/download/{pdf_filename}"
    
    appointment_data = {
        "appointment_date": req.appointment_date,
        "appointment_time": req.appointment_time,
        "doctor_notes": req.doctor_notes,
        "prescription_text": req.prescription_text,
        "pdf_url": download_url,
        "issued_at": datetime.now().isoformat()
    }
    
    sessions[req.session_id]["appointment"] = appointment_data
    return {"status": "success", "appointment": appointment_data}


@app.get("/api/v1/prescription/download/{filename}")
def download_prescription(filename: str):
    """Serves generated prescription PDFs to patients or doctors."""
    file_path = os.path.join(PRESCRIPTION_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename=filename)
    return {"error": "Prescription not found"}


@app.get("/api/v1/intake/session/{session_id}")
def get_single_session(session_id: str):
    """Allows a patient to check their registration status and download prescriptions."""
    if session_id in sessions:
        return sessions[session_id]
    return {"error": "Session not found"}


@app.get("/api/v1/intake/sessions")
def get_all_sessions():
    active_intakes = []
    for s_id, s_data in sessions.items():
        active_intakes.append({
            "session_id": s_id,
            "created_at": s_data.get("created_at"),
            "patient_name": s_data.get("patient_name", "Unknown"),
            "contact_number": s_data.get("contact_number", "N/A"),
            "contact_email": s_data.get("contact_email", "N/A"),
            "symptoms": s_data.get("symptoms", "None provided"),
            "documents_count": len(s_data.get("documents", [])),
            "documents": s_data.get("documents", []),
            "appointment": s_data.get("appointment")
        })
    return {"intakes": active_intakes}


@app.post("/api/v1/document/upload")
async def upload_document(session_id: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    extracted_text = ""
    try:
        if file.content_type == "application/pdf":
            reader = PdfReader(io.BytesIO(contents))
            for page in reader.pages:
                extracted_text += page.extract_text() or ""
        else:
            extracted_text = f"[Uploaded file: {file.filename}]"
    except Exception as e:
        extracted_text = f"Error extracting text: {str(e)}"

    doc_ref_id = f"doc-{uuid.uuid4().hex[:8]}"

    if session_id in sessions:
        sessions[session_id]["documents"].append({
            "filename": file.filename,
            "file_url": f"http://127.0.0.1:8000/api/v1/document/view/{file.filename}",
            "extracted_text": extracted_text,
            "fhir_id": doc_ref_id
        })

    return {
        "status": "success",
        "session_id": session_id,
        "filename": file.filename,
        "file_url": f"http://127.0.0.1:8000/api/v1/document/view/{file.filename}",
        "extracted_text": extracted_text
    }


@app.get("/api/v1/document/view/{filename}")
def view_document(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    return {"error": "File not found"}


@app.post("/api/v1/fhir/generate")
def generate_fhir_bundle(req: GenerateFHIRRequest):
    patient_id = f"pat-{uuid.uuid4().hex[:8]}"
    condition_id = f"cond-{uuid.uuid4().hex[:8]}"
    
    patient = Patient(
        id=patient_id,
        active=True,
        name=[{"use": "official", "text": req.patient_name}],
        telecom=[
            {"system": "phone", "value": req.contact_number},
            {"system": "email", "value": req.contact_email}
        ]
    )
    
    condition = Condition(
        id=condition_id,
        clinicalStatus=CodeableConcept(
            coding=[Coding(system="http://terminology.hl7.org/CodeSystem/condition-clinical", code="active")]
        ),
        subject={"reference": f"Patient/{patient_id}"},
        code=CodeableConcept(text=req.primary_symptom)
    )
    
    fhir_bundle = Bundle(
        id=f"bundle-{uuid.uuid4().hex[:8]}",
        type="transaction",
        identifier={"system": "http://medikiosk.ai/sessions", "value": req.session_id},
        entry=[
            BundleEntry(fullUrl=f"urn:uuid:{patient_id}", resource=patient, request={"method": "POST", "url": "Patient"}),
            BundleEntry(fullUrl=f"urn:uuid:{condition_id}", resource=condition, request={"method": "POST", "url": "Condition"})
        ]
    )
    
    return fhir_bundle.dict()

@app.get("/api/v1/patient/history")
def get_patient_history(contact: str):
    """Retrieves all past check-in sessions and issued prescriptions matching an email or phone number."""
    history = []
    clean_contact = contact.strip().lower()
    
    for s_id, s_data in sessions.items():
        email = s_data.get("contact_email", "").strip().lower()
        phone = s_data.get("contact_number", "").strip().lower()
        
        if clean_contact == email or clean_contact == phone:
            history.append({
                "session_id": s_id,
                "created_at": s_data.get("created_at"),
                "patient_name": s_data.get("patient_name"),
                "symptoms": s_data.get("symptoms"),
                "documents": s_data.get("documents", []),
                "appointment": s_data.get("appointment")
            })
            
    # Sort by newest first
    history.sort(key=lambda x: x["created_at"], reverse=True)
    return {"history": history}

# --- Authentication & Verification Schemas ---

class DoctorRegisterSchema(BaseModel):
    full_name: str
    email: str
    password: str
    license_number: str
    specialization: str
    hospital_name: str

class LoginSchema(BaseModel):
    email: str
    password: str

# In-Memory Database for Doctors
doctors_db = []

# --- Authentication & Admin Endpoints ---

@app.post("/api/auth/register-doctor")
def register_doctor(doctor: DoctorRegisterSchema):
    for d in doctors_db:
        if d["email"] == doctor.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    new_doctor = {
        "id": len(doctors_db) + 1,
        "full_name": doctor.full_name,
        "email": doctor.email,
        "hashed_password": hash_password(doctor.password),
        "license_number": doctor.license_number,
        "specialization": doctor.specialization,
        "hospital_name": doctor.hospital_name,
        "is_verified": False,
        "role": "doctor"
    }
    doctors_db.append(new_doctor)
    return {"message": "Application submitted! Awaiting hospital admin approval."}

@app.post("/api/auth/login")
def login(credentials: LoginSchema):
    doctor = next((d for d in doctors_db if d["email"] == credentials.email), None)
    if not doctor or not verify_password(credentials.password, doctor["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not doctor["is_verified"]:
        raise HTTPException(
            status_code=403, 
            detail="Account pending verification. Your credentials are under admin review."
        )
    
    token = create_access_token({"sub": doctor["email"], "role": doctor["role"], "id": doctor["id"]})
    return {"access_token": token, "token_type": "bearer", "doctor": doctor}

@app.get("/api/admin/pending-doctors")
def get_pending_doctors():
    return [d for d in doctors_db if not d["is_verified"]]

@app.post("/api/admin/verify-doctor/{doctor_id}")
def verify_doctor(doctor_id: int):
    for d in doctors_db:
        if d["id"] == doctor_id:
            d["is_verified"] = True
            return {"message": f"Doctor {d['full_name']} verified successfully."}
    raise HTTPException(status_code=404, detail="Doctor not found")