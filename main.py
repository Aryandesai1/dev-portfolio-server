from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://main.d1p3j54qjn3fm1.amplifyapp.com",
        "https://www.aryandesai34.com"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_email(name: str, email: str, message: str):
    msg = EmailMessage()
    msg['Subject'] = f"New Contact from {name}"
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg.set_content(f"From: {name} <{email}>\n\n{message}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is working!"}

@app.get("/projects")
def get_projects():
    return [
        
        {
            "title": "Rainbow Vista Art Inc. Entertainment Company Website",
            "description": "• UI/UX Design: Crafted modern, mobile-first layouts using React components and Bootstrap for responsiveness.\n• Component Architecture: Built reusable components for forms, event displays, and dynamic data handling.\n• API Integration: Integrated with a backend using Axios for data fetching and real-time updates.\n• Deployment: Deployed the frontend using AWS Amplify, with automatic builds and continuous deployment via GitHub integration.\n• Performance Optimization: Implemented lazy-loading, code-splitting, and optimized loading times for a smooth user experience.",
            "tags": ["React", "JavaScript", "Bootstrap", "AWS Amplify"],
            "image": "https://api.aryandesai34.com/static/project2.png"
        },


        {
            "title": "Virtual Reaility Reminiscene therapy",
            "description": "A VR application for reminiscence therapy. Made in Unity and ",
            "tags": ["VR", "Unity", "PHP", "MySQL", "WebGL"],
            "image": "https://api.aryandesai34.com/static/project1.png"
        },
        {
            "title": "ChatGPT integrated Chatbot Jarvis",
            "description": "A chatbot integrated with ChatGPT, capable of answering questions and performing tasks.",
            "tags": ["ChatGPT", "Python","Anaconda","Jupyter Notebook"],

        },
    ]
class ContactForm(BaseModel):
    name: str
    email: str
    message: str
    
@app.post("/contact")
def submit_contact(form: ContactForm):
    send_email(form.name, form.email, form.message)
    return {"message": "Email sent successfully"}

