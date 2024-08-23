from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import shutil
import uvicorn
import aspose.pdf as ap

app = FastAPI(title="PDF_AUTHENTICATOR",version="1.0.0")

@app.get("/")
def hello_api():
    return {"msg":"Hello FastAPI🚀"}

@app.post("/file/upload")
def upload_file(file: UploadFile):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    method = 2
    match method:
        case 1:
            ### Method 1
            mender = ap.facades.PdfFileMend()
            mender.bind_pdf(file.filename)
            mender.add_image("joinha.jpg", 1, 20.0, 130.0, 120.0, 190.0)
            authenticate_file = "autenticado_"+file.filename
            mender.save(authenticate_file)
            mender.close()
        
        case 2:
            ### Method 2
            document = ap.Document(file.filename)
            document.pages[1].add_image("assinatura.png", ap.Rectangle(20, 130, 120, 190, True))
            authenticate_file = "autenticado_"+file.filename
            document.save(authenticate_file)

    return FileResponse(path=file.filename,media_type="application/octet-stream",filename=authenticate_file)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
    
