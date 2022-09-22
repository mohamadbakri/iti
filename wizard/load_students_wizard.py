from odoo import models, fields


class LoadStudents(models.TransientModel):
    _name = "iti.load.students"

    date = fields.Date()

    def load_students(self):
        print("Called")
        pass
