# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

from .validate_utils import validate_stage_fields


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.constrains("stage_id")
    def _validate_stage_fields(self):
        validate_stage_fields(self)
