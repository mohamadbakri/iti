from odoo import models, fields


class ItiTrack(models.Model):
    _name = "iti.track"
    _description = "Iti Tracks"
    _rec_name = "track_name"
    # to disable creation of default four tables
    #_log_access = False

    track_name = fields.Char()
    open = fields.Boolean()
    students_ids = fields.One2many(
        'iti.student', 'track_id', string='Students')
