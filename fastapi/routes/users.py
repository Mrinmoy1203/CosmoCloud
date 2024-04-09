from fastapi import APIRouter,HTTPException,Query
from models.users import Student
from config.db import conn,db,collection
from schemas.users import userEntity, usersEntity
from bson import ObjectId

user=APIRouter()

@user.post('/students')
async def create_students(user: Student):
    student_dict=user.dict()
    result=collection.insert_one(student_dict)
    return {"inserted_id": str(result.inserted_id)}

@user.patch('/students/{id}')
async def update_student(student_id: str, student_update: Student):
    obj_id = ObjectId(student_id)
    existing_student = collection.find_one({"_id": obj_id})
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    update_operation = {"$set": student_update.dict(exclude_unset=True)}

    result = collection.update_one({"_id": obj_id}, update_operation)

    if result.modified_count == 1:
        return {"message": "Student updated successfully"}
    else:
        return {"message": "Failed to update student"}



@user.delete('/student/{id}')
async def delete_student(id: str ):
    # Convert the ID string to ObjectId
    obj_id = ObjectId(id)

    # Check if the student with the given ID exists
    existing_student = collection.find_one({"_id": obj_id})
    if existing_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Delete the student document from the collection
    result = collection.delete_one({"_id": obj_id})

    # Check if the deletion was successful
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "Failed to delete student"}


@user.get('/students')
async def get_students_from_country_and_min_age(
    country: str = Query(..., description="Country to filter students by"),
    min_age: int = Query(None, description="Minimum age of students to filter by")
):
    
    filter_criteria = {"address.country": country}
    if min_age is not None:
        filter_criteria["age"] = {"$gte": min_age}

    students = collection.find(filter_criteria)

    student_list = []
    for student in students:
        
        student['_id'] = str(student['_id'])
        student_list.append(student)


    if not student_list:
        raise HTTPException(status_code=404, detail=f"No students found matching the criteria")


    return student_list

@user.get('/students/{id}')
async def get_student_by_id(student_id: str):
    try:
        # Convert the ID string to ObjectId
        obj_id = ObjectId(student_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid student ID")

    # Query MongoDB to find the student with the given ID
    student = collection.find_one({"_id": obj_id})

    # Check if the student exists
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # Convert ObjectId to string for JSON serialization
    student['_id'] = str(student['_id'])

    # Return the student record
    return student