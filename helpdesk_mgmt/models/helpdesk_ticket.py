from odoo import models, fields, _


class HelpdeskTicket(models.Model):

    _name = 'helpdesk.ticket'
    _order = 'number desc'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    number = fields.Char(string='Ticket number', readonly=True)
    name = fields.Char(string='Title', required=True)
    description = fields.Text(required=True)
    user_id = fields.Many2one('res.users', string='Assigned user', default=lambda self: self.env.user)
    state = fields.Many2one('helpdesk.ticket.state', string='State') #TODO: default
    partner_id = fields.Many2one('res.partner')
    partner_name = fields.Char()
    partner_email = fields.Char()

    last_state_update = fields.Datetime()
    assigned_date = fields.Datetime()
    closed_date = fields.Datetime()

    tag_ids = fields.Many2many('helpesk.ticket.tag')
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )
    channel_id = fields.Many2one('helpdesk.ticket.channel', string='Channel')
    category_id = fields.Many2one('helpdesk.ticket.category', string='Category')
    team_id = fields.Many2one('helpdesk.ticket.team')
    priority_id = fields.Selection(selection=[
        ('0', _('Low')),
        ('1', _('Medium')),
        ('2', _('High')),
        ('3', _('Very High')),
    ], string='Priority', default='medium')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'website.support.ticket')],
                                     string="Media Attachments")
