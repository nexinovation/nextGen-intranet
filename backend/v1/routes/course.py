from flask import request, jsonify
from ..models.course import db, Course
from ..models.roles import Group
from . import course


# admin only route
@course.route("/", strict_slashes=False, methods=["POST"])
def create_course():
    try:
        data = request.get_json()
        if not data:
                return jsonify({"error": "Missing registration data"}), 400
        
        course = Course()
        err = course.validate_fields(['name'], data=data)
        if err:
                return jsonify(err), 400

        course_exist = Course.query.filter_by(name=data.get('name')).first()
        if course_exist:
            return jsonify({'error': f'Course {course_exist.name} already exists'}), 401

        for key, value in data.items():
            if hasattr(course, key):
                setattr(course, key, value)

        db.session.add(course)

        response_object = {
            "message": f"Course {course.name} registered successfully."
        }

        if not Group().query.filter_by(name="Group 1").first():
            group = Group(name="Group 1")
            db.session.add(group)
            response_object.update(group="new default Group `Group 1` created.")

        db.session.commit()

        return jsonify(response_object)

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "An unexpected error occurred"}), 500
