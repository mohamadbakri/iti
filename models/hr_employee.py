from odoo import models, fields


class HrEmployeeInherit(models.Model):
    # it is perefirable not to include _name it will use hr.employee by default
    _name = "hr.employee"
    _inherit = "hr.employee"

    national_id_number = fields.Char()
    # national_id_number = fields.Char(required=True)
