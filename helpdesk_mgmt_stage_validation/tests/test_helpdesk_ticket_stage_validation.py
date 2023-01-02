# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestHelpdeskStageValidation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.stage = cls.env["helpdesk.ticket.stage"]
        cls.helpdesk_ticket = cls.env["helpdesk.ticket"]
        cls.ir_model_fields = cls.env["ir.model.fields"]
        # Get some fields to use in the stages
        cls.ticket_field = cls.ir_model_fields.search(
            [("model", "=", "helpdesk.ticket"), ("name", "=", "assigned_date")]
        )
        cls.stage_ticket_default = cls.stage.create(
            {
                "name": "Helpdesk Ticket Stage Default",
            }
        )
        cls.stage_ticket_assigned = cls.stage.create(
            {
                "name": "Helpdesk Ticket Assigned",
                "validate_field_ids": [(6, 0, [cls.ticket_field.id])],
            }
        )
        cls.ticket = cls.helpdesk_ticket.create(
            {
                "name": "Helpdesk Ticket",
                "description": "Helpdesk Ticket Description",
                "stage_id": cls.stage_ticket_default.id,
            }
        )

    def get_validate_message(self, stage):
        stage_name = stage.name
        field_name = fields.first(stage.validate_field_ids).name
        return 'Cannot move to stage "%s" until the "%s" field is set.' % (
            stage_name,
            field_name,
        )

    def test_helpdesk_ticket_stage_validation(self):
        validate_message = self.get_validate_message(self.stage_ticket_assigned)
        with self.assertRaisesRegex(ValidationError, validate_message):
            self.ticket.write({"stage_id": self.stage_ticket_assigned.id})
