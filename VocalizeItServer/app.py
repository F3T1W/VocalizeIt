from fastapi import FastAPI, File, UploadFile
import os
from pdfminer.high_level import extract_text

app = FastAPI()

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        file_location = f"{UPLOAD_FOLDER}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        extracted_text = extract_text(file_location)
        text_filename = f"{UPLOAD_FOLDER}/{file.filename.rsplit('.', 1)[0]}.txt"

        with open(text_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)

        return {"message": "File processed", "txt_file": text_filename}
    else:
        return {"error": "Only PDF files are allowed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)