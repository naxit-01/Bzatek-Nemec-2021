import uvicorn
from fastapi import FastAPI, Query, Cookie
import json
import os
from typing import Optional

app = FastAPI()


@app.get("/")
def root(params: Optional[str] = Query(None, max_length=50), UserID: Optional[str] = Cookie(None), UserType: Optional[str] = Cookie(None)):
    if UserType == "student" or UserType == "teacher":
        return {"hello world": 'root'}
    return False

@app.get('/student/{student_id}')
def student(student_id,params: Optional[str] = Query(None, max_length=50), UserID: Optional[str] = Cookie(None), UserType: Optional[str] = Cookie(None)):
	if UserType != "student" and UserType != "teacher":
		return "Not authorized for this data."
	else:

		if not student_id and UserType == "student":
			student_id = UserID
		elif not student_id:
			student_id = 0 #Default, or redirect to 404

		return {
			"type": 'student',
			"id": student_id,
			"data": 'some data about student'}

	return False

@app.get('/teacher/{teacher_id}')
def student(teacher_id,params: Optional[str] = Query(None, max_length=50), UserID: Optional[str] = Cookie(None), UserType: Optional[str] = Cookie(None)):
	if UserType != "teacher":
		return "Not authorized for this data."
	else:

		if not teacher_id:
			teacher_id = UserID

		return {
			"type": 'teacher',
			"id": teacher_id,
			"data": 'some data about teacher'}

	return False

@app.get('/rozvrh/{group_id}')
def timeSchedule(group_id,params: Optional[str] = Query(None, max_length=50)):
    print(params)
    #data = json.loads(params)

    if not group_id:
        group_id = 0 #Default or redirect to 404

    return {
        "type":"time schedule",
        "id": group_id,
        "data": "groups time schedule"
        }

    return False

@app.get('/group/{group_id}')
def group(group_id,params: Optional[str] = Query(None, max_length=50), UserID: Optional[str] = Cookie(None), UserType: Optional[str] = Cookie(None)):
    '''Old version'''
    data = json.loads(params)
    if UserType != "teacher":
        return {
            "type":"group",
            "id": group_id,
            "data": "some data about group"
        }
    return False

@app.get('/reset/{host}/{port}')
async def reset(host,port,params: Optional[str] = Query(None, max_length=50), UserID: Optional[str] = Cookie(None), UserType: Optional[str] = Cookie(None)):
    #Can log admin ID, who changed the adress
    if UserType == "admin":
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
