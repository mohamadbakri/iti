from odoo import models, fields, api
from odoo.addons.hr_holidays.models.hr_leave import DummyAttendance
from odoo.exceptions import UserError, ValidationError


class ItiStudent(models.Model):
    _name = "iti.student"
    _description = "Iti Students"
    # to disable creation of default four tables
    # _log_access = False

    name = fields.Char()
    age = fields.Integer()
    birth_date = fields.Date()
    salary = fields.Integer()
    tax = fields.Float()
    # store = True to save on db
    computed_tax = fields.Float(compute='_calc_tax', store=True)
    gender = fields.Selection([
        ("m", "Male"),
        ("f", "Female"),
    ])
    student_state = fields.Selection([
        ('nw', "New"),
        ('ps1', "Passed First Interview"),
        ('ps2', "Passed Second Interview"),
        ('ac', "Accepted"),
        ('r', "Rejected"),
    ], default="nw")
    military_certificate = fields.Binary()
    cv = fields.Binary()
    image = fields.Binary()
    info = fields.Text()
    accepted = fields.Boolean()
    bio = fields.Html()
    registration_at = fields.Datetime()
    track_id = fields.Many2one("iti.track")
    track_open = fields.Boolean(related="track_id.open")
    # track_open = fields.Boolean(related="track_id.open" readonly=False)
    skills_ids = fields.Many2many("iti.skill")
    log_history_ids = fields.One2many("iti.log.history", "student_id")

    @api.depends("salary")
    def _calc_tax(self):
        for rec in self:
            rec.computed_tax = rec.salary * 0.1

    @api.onchange("salary")
    def onchange_salary(self):
        if self.salary:
            self.tax = self.salary * .100

    @api.onchange("accepted")
    def onchange_accepted(self):
        if self.accepted:
            self.salary = 100
        return {
            'domain': {
                "track_id": [('open', '=', True)]
            },
            'warning': {
                "title": "Hello",
                "message": f"The Salary Changerd to {self.salary}"}
        }

    def change_state(self):
        # To ensure that self hold only one record use
        # self.ensure_one()
        for record in self:
            if self.student_state == 'nw':
                self.student_state = 'ps1'
            elif self.student_state == 'ps1':
                self.student_state = 'ps2'

        description = f"State changed to {self.student_state}"
        result = self.log_history_ids.search([
            ('description', '=', description)
        ])
        if not result:
            self.env['iti.log.history'].create({
                "description": f"State changed to {self.student_state}",
                "student_id": self.id
            })

    def reset_state(self):
        self.student_state = 'nw'

    # Override CRUD functions and Validations,
    # Validations,
    @api.model
    def create(self, vals):
        if self.search([("name", "=", vals.get("name"))]):
            raise UserError("Duplicated Name")
        if vals.get("age") < 20:
            raise UserError("Wrong Age")
        new_student = super().create(vals)
        # Integrate to other site from odoo site
        # requsts.post("http://other_system.com/students",
        #              json={"name": new_student.name, "odoo_id": new_student.id})
        return new_student

    # To load date form other systems
    # recorded video minutes 2:00 day05
    # Run through cron job or scheduled action
    # def load_students_from_external_api(self):
    #     students -= requests.get("https://other_sytetm.com/students")
    #     for student in students:
    #         self.create(student)

    def write(self, vals):
        age = vals.get("age")
        if age and age < 20:
            raise UserError("Wrong Age")
        return super().write(vals)

    def unlink(self):
        if self.student_state != "nw":
            raise UserError(
                "You can't delete students with state other than New")
        super().unlink()

    """
    search 
    browse
    """
    @api.constrains("info")
    def _validate_info(self):
        if self.info and len(self.info) < 20:
            raise ValidationError(
                "Info length should be greater than 20 characters")

    # More faster than api.constrains
    _sql_constraints = [
        # ('duplicate_name', 'UNIQUE(name)', 'Name already exists'),
        # ('wrong_age', 'CHECK(age >= 20, age <= 40)', 'Wrong Age'),
        ('not_fair_salary', 'CHECK(salary >= 2000)', 'Not Fair Salary'),
    ]

    # def create(self, vals):
    # if not vals.get("name"):
    #     raise
    # =========================
    # new_student = super().create(vals)
    # new_student.name += "Hello"
    # return new_student
    # =========================
    # the most important in create function is to raturn an object with an id
    # return DummyStudent()
    # return super().create(vals)

    # def write(self, vals):
    #     if self.student_state == "ps1":
    #         raise UserError(
    #             "You can't update students with state other than New")
    #     super().write(vals)
    #     # Or return
    #    # return super().write(vals)


class LogHistory(models.Model):
    _name = "iti.log.history"

    description = fields.Text()
    student_id = fields.Many2one("iti.student")


class DummyStudent:
    # to be returned for create function
    def __inti__(self):
        self.id = 5
