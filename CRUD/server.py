
from pymongo import MongoClient
from bson import binary, Code, ObjectId
from bson.json_util import dumps
from flask import Flask, request, make_response
# from flask_restful import Resource, Api
import json 

app = Flask(__name__)
mongo = MongoClient("localhost", 27017)
app.db = mongo.local

class NewJSONEncoder(json.JSONEncoder):
	def default(self, o):
		"""Flatten ObjectId object in a course"""

		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self,o)

def error_response(error_message):
	"""Return an error object containing specified error"""
	return json.dumps({"error": error_message})


@app.route('/courses', methods=['POST'])
def post_course():
	""" Post a course document to course collection database. Course must have a name and number."""

	# Collection of course documents in database
	course_collection = app.db.courses
	# Course dictionary(from request) trying to be posted to database
	course_dict = request.json

	# Check if 'course_dict' has 'name' and 'number' keys. (necessary values)
	if "name" in course_dict and "number" in course_dict:
		try:
			# Try to update name and number values in 'course_dict' to the expected types for our database.
			course_dict["name"] = str(course_dict["name"])
			course_dict["number"] = int(course_dict["number"])
		except ValueError:
			# Return error if name/number value conversion to necessary type failed. 
			return(error_response("Incorrect data type for name and/or number value"), 422, None)

		name = course_dict["name"]
		number = course_dict["number"]

		# Check if name is empty or whitespace and if number is valid
		if name and name.strip() and number :
			# Insert 'course_dict' as document to database
			result = course_collection.insert_one(course_dict)
			return("Course Posted", 201, None)
 
	return(error_response("Missing field/fields: name and/or number"), 400, None)

@app.route('/courses', methods=['GET'])
def get_course_with_number():
	"""Finds and returns course document with matching number from database if found, or returns error object.
	   ** If multiple matches occur, will return array of matched courses **
	"""

	# Get number parameter value from request arguments. If present try to convert to integer 
	number = request.args.get("number",type=int)

	if number is not None:
		# Courses collection from database
		course_collection = app.db.courses
		# Try to find course with matching number
		# found_course = course_collection.find_one({"number": number})
		matched_course = course_collection.find({"number": number})
		multiple_courses_matched = []

		if matched_course.count() is 0:
			return(error_response("Course not found"), 404, None)

		for course in matched_course:
			if course is not None and matched_course.count() == 1:
				# Encode course found and return it as JSON
				course = NewJSONEncoder().encode(course)
				return(course, 200, None)
			elif course is not None and matched_course.count() > 1:
				multiple_courses_matched.append(course)

		encoded_courses = NewJSONEncoder().encode(multiple_courses_matched)
		return(encoded_courses, 200, None)
	
	#'number' is empty or not an integer
	return(error_response("Number parameter value invalid/missing"), 400, None)

@ app.route('/all-courses', methods=['GET'])
def get_all_courses():
	"""Returns array of all courses in database or error object if database is empty."""

	# Courses collection from database
	course_collection = app.db.courses
	# Finds all courses in collection
	courses = course_collection.find({})

	course_objects_list = []

	for course in courses:
		course_objects_list.append(course)
		print(len(course_objects_list))

	if len(course_objects_list) > 0:
		response = NewJSONEncoder().encode(course_objects_list)
		return(response, 200, None)

	return(error_response("No courses found in database"), 404, None)

@app.route('/count-courses', methods=['GET'])
def count_courses():
	""" Returns dict containing KEY: "count", Value: total count of courses """
	# Courses collection from database
	course_collection = app.db.courses
	# Finds all courses in collection
	all_courses = course_collection.find({})

	count = str(all_courses.count())
	response = json.dumps({"count": count})

	return(response, 200, None)


if __name__ == '__main__':
    # app.run()
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)






