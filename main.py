from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

save_folder = 'saved_txt'


@app.get("/")
def read_form(request: Request):
	return templates.TemplateResponse("form.html", {"request": request})


@app.post("/save_data/")
def save_data(request: Request, file_name: str = Form(...), napolnenie: str = Form(...)):
	if not file_name.lower().endswith(".txt"):
		raise HTTPException(status_code=400, detail="only .txt")
	with open(f"saved_txt/{file_name}", "w") as f:
		f.write(napolnenie)
	return templates.TemplateResponse("succes.html", {"request": request, "file_name": file_name})


@app.get("/list_files/")
def list_files(request: Request):
	file_names = get_txt_file_list()
	return templates.TemplateResponse("list_files.html", {"request": request, "file_names": file_names})


@app.get("/view_file/{file_name}")
def view_file(request: Request, file_name: str):
	file_path = os.path.join(save_folder, file_name)
	with open(file_path, "r") as file_object:
		file_content = file_object.read()

	return templates.TemplateResponse("view_file.html",
	                                  {"request": request, "file_name": file_name, "file_content": file_content})


def get_txt_file_list():
	txt_files = [file for file in os.listdir(save_folder) if file.lower().endswith(".txt")]
	return txt_files
