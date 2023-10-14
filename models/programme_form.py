from odoo import models, fields, api, _
from datetime import datetime, timedelta


class ProgrammeForm(models.Model):
    _name = 'programme.form'
    _description = 'programme'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date', required=True)
    hall_id = fields.Many2one('programme.halls', string='Hall', required=True)
    location = fields.Char(string='Location', related='hall_id.location')
    programme_coordinators = fields.Many2many('res.users', string='Programme Coordinators')
    selected_staffs_only = fields.Boolean(string='Selected Staffs')
    all_staffs = fields.Boolean(string='All Staffs')
    selected_staffs = fields.Many2many('hr.employee', string='Staffs')
    requirements = fields.Text(string='Requirements')
    state = fields.Selection([
        ('draft', 'Draft'), ('scheduled', 'Scheduled'),
    ], default='draft', tracking=True, copy=False, string='Status')

    @api.onchange('selected_staffs_only', 'all_staffs')
    def onchange_selected_staffs_only(self):
        if self.selected_staffs_only == False:
            self.selected_staffs = False
        if self.selected_staffs_only == True:
            self.all_staffs = False
        if self.all_staffs == True:
            self.selected_staffs = False
            self.selected_staffs_only = False

    @api.depends('make_visible_user_pro')
    def get_make_visible_user_pro(self):
        print('kkkll')
        user_crnt = self.env.user.id

        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('logic_programs.programme_users'):
            self.make_visible_user_pro = True

        else:
            self.make_visible_user_pro = False

    make_visible_user_pro = fields.Boolean(string="Pro User", compute='get_make_visible_user_pro')

    def action_schedule(self):
        for record in self:
            users = []
            if record.programme_coordinators:
                user_id = record.programme_coordinators
                # users.append(user_id)
                for j in user_id:
                    print(j, 'users')
                    record.activity_schedule('logic_programs.mail_programme_activity', user_id=j.id,
                                             note=f' {record.name} Programme Alert. Save the date - {record.date}')
            if record.selected_staffs:
                staffs = record.selected_staffs
                for rec in staffs:
                    print(rec, 'staffs')
                    record.activity_schedule('logic_programs.mail_programme_activity', user_id=rec.user_id.id,
                                             note=f' {record.name} Programme Alert. Save the date - {record.date}')
            if record.all_staffs == True:
                res_user = self.env['res.users'].search([])
                for user in res_user:
                    if user.has_group('logic_programs.programme_users'):
                        record.activity_schedule('logic_programs.mail_programme_activity', user_id=user.id,
                                                 note=f' {record.name} Programme Alert. Save the date - {record.date}')

        self.state = 'scheduled'

    def remove_activity(self):
        rec = self.env['programme.form'].search([])
        for i in rec:
            if i.date:
                # Get the current date
                current_date = datetime.now().date()

                # Calculate the date one day from now
                one_day_later = i.date + timedelta(days=1)
                if current_date == one_day_later:
                    activity_id = self.env['mail.activity'].search(
                        [('res_id', '=', i.id), (
                            'activity_type_id', '=', self.env.ref('logic_programs.mail_programme_activity').id)])
                    print(activity_id, 'activity_id')
                    activity_id.unlink()
                #     print('one day later')
                #     batches = self.env['mail.activity'].search(
                #         [(('res_id', '=', i.id),
                #           'activity_type_id', '=', i.env.ref('logic_programs.mail_programme_activity').id)])
                #     print(batches, 'batches')
                #     batches.sudo().unlink()
                # else:
                #     print('not one day later')
                # print(one_day_later, 'one_day_later')
                # print(i.date, 'record.date')
                # print(current_date, 'current_date')
