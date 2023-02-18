import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.templating import Jinja2Templates
from aiohttp import web
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory='templates/')

class Item1(BaseModel):
    file_name: str

class Item(BaseModel):
    name: str
    roll: int    

kaldi_model_path='/home/vijay/te'


@app.post("/upload")
async def asr_uploadfile(form_data: UploadFile):

    os.chdir(kaldi_model_path)
    os.system("rm audios/*")
    open("audios/" + form_data.filename, 'wb').write(form_data.file.read())
    os.system('ffmpeg -loglevel warning -hide_banner -stats -i audios/{0} -ac 1 -ar 16000 audios/speech.wav'.format(form_data.filename))
    ret = os.system('bash demo.sh')
    with open("decoded_text") as my_file:
        decoded_text = my_file.read()
    return decoded_text.rstrip()


@app.post("/asr")
async def asr_dashboard(item1: Item1):

    src = kaldi_model_path+'/'+"audios/" + {0}.format(item1.file_name)
    dst = kaldi_model_path+'/'+"audios/speech_recorded.wav"
    dest = shutil.copyfile(src, dst)
    os.chdir(kaldi_model_path)
    os.system('ffmpeg -loglevel warning -hide_banner -stats -i audios/speech_recorded.wav -ac 1 -ar 16000 audios/speech.wav')
    ret = os.system('bash demo.sh')
    ret = os.system('cat decoded_text')
    with open("decoded_text") as my_file:
        ret_text = my_file.read()

    temr_ret = {"asr_output": ret_text}
    os.system("rm audios/*.wav*")

    return temp_ret


@app.get("/test/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/asr/")
async def get_asr(request: Request):
    return templates.TemplateResponse('asr_dashboard.html',{'request':request})

@app.post("/test_post/")
async def test_post(item: Item):
    return {"Success":'ok'}
