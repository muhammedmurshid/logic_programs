from odoo import models, fields, api, _


class ProgrammeHalls(models.Model):
    _name = 'programme.halls'
    _description = 'Hall'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    size = fields.Selection([('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], string='Size')
    location = fields.Char(string='Location', required=True)
    capacity = fields.Integer(string='Capacity')
    layout = fields.Selection(
        [('theater_style_sitting', 'Theater Style Sitting'), ('class_room_style', 'Class Room Style Sitting'),
         ('banquet_style', 'Banquet Style Sitting'), ('open_floor', 'Open Floor')],
        string='Layout')
    # amenities
    stage = fields.Boolean(string='stage')
    lighting = fields.Boolean(string='lighting')
    sound_system = fields.Boolean(string='sound system')
    wifi = fields.Boolean(string='wifi')
    parking = fields.Boolean(string='parking')

