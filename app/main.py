from fastapi import FastAPI,Path
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


students = {
    1: {"name": "John", 
        "age": 22,
        "year":2022
        }
}

class Student(BaseModel):
    name: str
    age: int
    year: int

class UpdateStudent(BaseModel):
    name:Optional[str]=None
    age: Optional[int]=None
    year: Optional[int]=None

@app.get("/")
def root():
    return {"message": "hi,k how are you"}

@app.post("/echo")
def echo(data:str):
    return {"you sent": data}

@app.get("/students/{student_id}")
def get_student(student_id: int=Path(...,description="The ID of the student to get")):
    return students[student_id]

@app.get("/get-by-name/")
def get_student_by_name(name: str=None):
    for student in students:
        if students[student]["name"] == name:
            return students[student]
    return {"Data": "not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id : int, student:Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id : int, student:UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int ):
    if student_id not in students:
        return {"msg":"not there"}
    del students[student_id]
    return {"msg":"deleted"}