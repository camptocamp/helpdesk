# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._run_stage_server_action()
        return records

    def write(self, vals):
        res = super().write(vals)
        if "stage_id" in vals:
            self._run_stage_server_action()
        return res

    def _run_stage_server_action(self):
        for record in self:
            action_id = record.stage_id.action_id
            if not action_id:
                continue
            ctx = {
                "active_model": self._name,
                "active_id": record.id,
            }
            action_id.with_context(**ctx).run()
