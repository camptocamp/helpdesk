# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HelpDeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    warranty_end_date = fields.Date(
        related="equipment_id.warranty_end_date",
        string="Warranty End Date",
        readonly=True,
        stored=True,
    )
