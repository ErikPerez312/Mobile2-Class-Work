from flask import Flask, request
from pymongo import MongoClient
import json
import pdb

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.local
db = app.db


class NewJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/courses', methods=['POST'])
def course_route():
    # data = request.data
    # dataDict = json.loads(data)
    # print(dataDict)
    courses_path = app.db.courses
    # inset into mongo db
    new_course = courses_path.insert_one({"name": "ENT", "number": 103}).inserted_id
    new_course
    print("Insert data successfully")
    db.collection_names(include_system_collections=False)
    responce = NewJSONEncoder().encode(new_course)
    return (None, 201, None)


@app.route('/courses', methods=['GET'])
def get_course_route():
    course_num_dict = request.args
    courses_path = app.db.courses
    course_num = int(course_num_dict['number'])
    result = courses_path.find_one({'number': course_num})
    response_json = NewJSONEncoder().encode(result)
    return (response_json, 200, None)


@app.route('/allCourses', methods=['GET'])
def all_courses():
    courses_path = app.db.courses
    result = courses_path.find({})
    for document in result:
        return document


@app.route('/person')
def person_route():
    # pdb.set_trace()
    json_person = {"name": "Erik", 'age': 19, "gender": "male"}
    json_ = json.dumps(json_person)
    return (json_, 200, None)


# CHALLENGE 1:
@app.route('/my_page')
def my_page_route():
    return "Do it anyway"


# CHALLENGE 2 & 3:
@app.route('/my_pets', methods=['GET', 'POST'])
def my_pets_route():
    if request.method == "POST":
        pets = json.dumps(request.json)
        return(pets, 200, None)
    else:
        json_pets = [{"name": "Sosa", "color": "tan", "species": "dog"},
                     {"name": "Hannah", "color": "white", "species": "cat"}]
        pets = json.dumps(json_pets)
        return (pets, 200, None)


if __name__ == '__main__':
    app.config["TRAP_BAD_REQUEST_ERRORS"] = True
    app.run(debug=True)
