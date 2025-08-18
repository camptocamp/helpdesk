# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FSMEquipment(models.Model):
    _inherit = "fsm.equipment"

    helpdesk_ticket_ids = fields.One2many("helpdesk.ticket", "equipment_id")
    helpdesk_ticket_count = fields.Integer(compute="_compute_helpdesk_ticket_count")

    @api.depends("helpdesk_ticket_ids")
    def _compute_helpdesk_ticket_count(self):
        for record in self:
            record.helpdesk_ticket_count = len(record.helpdesk_ticket_ids)

    def _force_stage_change(self, new_stage):
        # check if the user is in the group to force the stage change
        if self.env.user.has_group("fieldservice.group_fsm_equipment"):
            self.sudo().write({"stage_id": new_stage})
        else:
            self.write({"stage_id": new_stage})
