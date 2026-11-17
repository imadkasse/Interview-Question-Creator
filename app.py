from fastapi import FastAPI, Form, Request, Response, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import os
import aiofiles
import json
import csv
from src.helper import chain
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get('/health')
async def health():
    return {'status':"ok", 'msg':"every thing is good "}

@app.post("/upload")
async def upload_pdf(request: Request, pdf_file: bytes = File(...), filename: str = Form(...)):
    base_folder = 'static/docs/'
    
    # استخدام os.makedirs لتفادي الأخطاء إذا كان المجلد موجوداً مسبقاً
    os.makedirs(base_folder, exist_ok=True)
    pdf_filename = os.path.join(base_folder, filename)

    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)
 
    # الطريقة الأبسط: إرجاع Dictionary مباشرة
    return {
        "msg": "success",
        "pdf_filename": pdf_filename
    }


def get_csv(file_path):
    retrieval_chain, ques_list = chain(file_path)
    base_folder = 'static/output/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    output_file = f"{file_path}_QA.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"])  # Writing the header row

        for question in ques_list:
            print("Question: ", question)
            res = retrieval_chain.invoke({
                "input": question
            })
            answer =res['answer']
            print("Answer: ", answer)
            print("--------------------------------------------------\n\n")

            # Save answer to CSV file
            csv_writer.writerow([question, answer])
    return output_file




@app.post("/analyze")
async def chat(request: Request, pdf_filename: str = Form(...)):
    cleaned_path = pdf_filename.lstrip("/\\")
    file_path = Path.cwd() / cleaned_path
    print("Resolved File Path:", file_path)
    output_file = get_csv(file_path)
    response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
    res = Response(response_data)
    return res