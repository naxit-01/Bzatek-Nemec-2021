import uvicorn
from fastapi import FastAPI, Query
import json
import os
from typing import Optional

app = FastAPI()

#authorizacni postup pro router (jenom router ma pristup k api a tady je basic metoda)
sec_token_admin="asdfadmin"
sec_token_teacher="asdfteacher"
sec_token_student="asdfstudent"

def authorize(token):
    if token==sec_token_admin:
        return 'admin'
    if token==sec_token_teacher:
        return 'teacher'
    if token==sec_token_student:
        return 'student'
    return None

@app.get("/")
def root(params: Optional[str] = Query(None, max_length=50)):
    data = json.loads(params)
    if authorize(data['token'])=='admin' or authorize(data['token'])=='teacher' or authorize(data['token'])=='student':
        return {"hello world": 'root'}
    return False

@app.get('/student/{student_id}')
def student(student_id,params: Optional[str] = Query(None, max_length=50)):
    data = json.loads(params)
    if authorize(data['token'])=='admin' or authorize(data['token'])=='teacher' or authorize(data['token'])=='student':
        return {
            "type": 'student',
            "id": student_id,
            "data": 'some data about student'}
    return False

@app.get('/teacher/{teacher_id}')
def student(teacher_id,params: Optional[str] = Query(None, max_length=50)):
    data = json.loads(params)
    if authorize(data['token'])=='admin' or authorize(data['token'])=='teacher' or authorize(data['token'])=='student':
        return {
            "type": 'teacher',
            "id": teacher_id,
            "data": 'some data about teacher'}
    return False

@app.get('/rozvrh/{group_id}')
def timeSchedule(group_id,params: Optional[str] = Query(None, max_length=50)):
    data = json.loads(params)
    if authorize(data['token'])=='admin' or authorize(data['token'])=='teacher' or authorize(data['token'])=='student':
        return {
            "type":"time schedule",
            "id": group_id,
            "data": "groups time schedule"
        }
    return False

@app.get('/group/{group_id}')
def group(group_id,params: Optional[str] = Query(None, max_length=50)):
    data = json.loads(params)
    if authorize(data['token'])=='admin' or authorize(data['token'])=='teacher' or authorize(data['token'])=='student':
        return {
            "type":"group",
            "id": group_id,
            "data": "some data about group"
        }
    return False

@app.get('/reset/{host}/{port}')
async def reset(host,port,params: Optional[str] = Query(None, max_length=50)):
    data = json.loads(params)
    if authorize(data['token'])=='admin':
        data={
        'host': host,
        'port': port,
        }

        with open(os.path.join(os.path.dirname(__file__), "settings.txt"), 'w') as outfile:
            json.dump(data, outfile)

        uvicorn.run(app, host=host, port=int(port))
        return True
    return False

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "settings.txt")) as json_file:
        data = json.load(json_file)
        uvicorn.run(app, host=data['host'], port=int(data['port']))