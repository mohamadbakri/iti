from odoo import models, fields


class ItiSkill(models.Model):
    _name = "iti.skill"
    _description = "Iti Skills"
    _rec_name = "skill_name"
    # to disable creation of default four tables
    #_log_access = False

    skill_name = fields.Char()
    # students_ids = fields.One2many(
    #     'iti.student', 'track_id', string='Students')
