import time
from typing import List

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import crud, database, schemas
from database import db_state_default
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

sleep_time = 10

# disease_info = pd.read_csv('disease_info.csv' , encoding='cp1252')
# supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252')

# model = CNN.CNN(40)    
# model.load_state_dict(torch.load("plant_disease_model_1.pt",map_location=torch.device("cpu")))
# model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()

def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/predict")
async def root(request: Request):
    return templates.TemplateResponse("action.html", {"request":request})

@app.get("/sensors/{name}", response_model=schemas.Sensor, dependencies=[Depends(get_db)])
async def get_sensor(name: str):
    val = crud.get_sensor_value(name)
    if val is None:
        raise HTTPException(404, {"error":"Sensor not found"})
    return val

@app.get("/sensors", response_model=List[schemas.Sensor], dependencies=[Depends(get_db)])
async def get_sensor():
    val = crud.get_all_sensors()
    return val

@app.get("/configs/{name}", response_model=schemas.Sensor, dependencies=[Depends(get_db)])
async def get_config(name: str):
    val = crud.get_config_value(name)
    if val is None:
        raise HTTPException(404, {"error":"Config not found"})
    return val

@app.get("/configs", response_model=List[schemas.Sensor], dependencies=[Depends(get_db)])
async def get_sensor():
    val = crud.get_all_configs()
    return val

# @app.post("/predict")
# async def predict(file: bytes = File()):
#     with open('predict.JPG','wb') as f:
#         f.write(file)
#     print(len(file))
#     # print(file_path)
#     pred = prediction('predict.JPG')
#     title = disease_info['disease_name'][pred]
#     description =disease_info['description'][pred]
#     prevent = disease_info['Possible Steps'][pred]
#     supplement_name = supplement_info['supplement name'][pred]
#     return {
#         'disease': {
#             'name':title,
#             'description':description,
#             'prevention':prevent
#         },
#         'supplement': {
#             'name':supplement_name
#         }
#     }