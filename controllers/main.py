from odoo.http import Controller, request, route


class StudentController(Controller):
    # HTTP
    @route("/students", auth="user", cors="*", csrf=False, type="http", methods=["GET"])
    # @route("/students", auth="user or public or none", cors="*", csrf=false, type="json", methods=["get"])
    def get_students(self):
        students = request.env["iti.student"].search([])
        qweb_context = {
            "students": students
        }
        # return "<h1>hello world!</h1>"
        return request.render("iti.list_students_template", qweb_context)

    # API
    @route("/api/students", auth="user", cors="*", csrf=False, type="json", methods=["GET"])
    def get_all_students(self):
        students = request.env["iti.student"].search([])
        # Make your own Serializer
        serialized_students = []
        for s in students:
            serialized_students.append({
                "id": s.id,
                "name": s.name,
                "age": s.age,
                "salary": s.salary,
            })
        return {
            "students": serialized_students
        }

    @route("/api/students/<int:s_id>", auth="user", cors="*", csrf=False, type="json", methods=["GET"])
    def get_student(self, s_id):
        student = request.env["iti.student"].browse(s_id)
        # Make your own Serializer
        return {
            "name": student.name,
            "age": student.age,
            "salary": student.salary,
        }

    @route("/api/students/<int:s_id>", auth="user", cors="*", csrf=False, type="json", methods=["DELETE"])
    def delete_student(self, s_id):
        student = request.env["iti.student"].browse(s_id)
        student.unlink()
        # Make your own Serializer
        return {
            "deleted": True,
        }

    @route("/api/students", auth="user", cors="*", csrf=False, type="json", methods=["POST"])
    def create_student(self, name, age, salary):
        vals = {
            "name": name,
            "age": age,
            "salary": salary
        }

        new_student = request.env["iti.student"].create(vals)
        vals.update(id=new_student.id)
        return vals

    @route("/api/students/<int:s_id>", auth="user", cors="*", csrf=False, type="json", methods=["PATCH"])
    def update_student(self, s_id, **kwargs):
        student = request.env["iti.student"].browse(s_id)
        student.write(kwargs)
        return kwargs


"""
METHOD:GET 
http://localhost:8069/web/session/authenticate
{
    "jsonrpc": "2.0",
    "params": {
        "db": "odoo15",
        "login": "admin",
        "password": "admin"
    }
}

"""
"""
api five end points
- get_all                /students            GET
- get_single             /sutdents/<id>       GET
- create                 /students            POST 
- update                 /students/<id>       UPDEAT/PUT
- delete                 /students/<id>       DELETE
"""
