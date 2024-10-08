from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import os
from pdfminer.high_level import extract_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
os.makedirs(desktop_path, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):

        temp_pdf_path = os.path.join(desktop_path, "temp_uploaded_file.pdf")
        with open(temp_pdf_path, "wb") as temp_pdf:
            temp_pdf.write(await file.read())

        text = extract_text(temp_pdf_path)

        os.remove(temp_pdf_path)

        file_index = 1
        text_file_location = os.path.join(desktop_path, f"{file_index}.txt")
        while os.path.exists(text_file_location):
            file_index += 1
            text_file_location = os.path.join(desktop_path, f"{file_index}.txt")

        with open(text_file_location, "w", encoding="utf-8") as text_file:
            text_file.write(text)

        return {"message": f"Text saved in {file_index}.txt on your desktop!"}
    else:
        return {"error": "Only PDF files are allowed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
