# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class HelpdeskTicketStageServerAction(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(HelpdeskTicketStageServerAction, cls).setUpClass()
        cls.ServerAction = cls.env["ir.actions.server"]
        cls.HelpdeskTicket = cls.env["helpdesk.ticket"]
        cls.HelpdeskTicketStage = cls.env["helpdesk.ticket.stage"]
        cls.field = cls.env["ir.model.fields"]._get(cls.HelpdeskTicket._name, "user_id")
        cls.server_action_helpdesk_ticket = cls.ServerAction.create(
            {
                "name": "Helpdesk Ticket Server Action",
                "model_id": cls.env.ref("helpdesk_mgmt.model_helpdesk_ticket").id,
                "state": "object_write",
                "fields_lines": [
                    (
                        0,
                        0,
                        {
                            "col1": cls.field.id,
                            "evaluation_type": "value",
                            "value": cls.env.user.id,
                        },
                    )
                ],
            }
        )
        cls.helpdesk_ticket_stage_1 = cls.HelpdeskTicketStage.create(
            {"name": "Stage 1", "sequence": 1}
        )
        cls.helpdesk_ticket_stage_2 = cls.HelpdeskTicketStage.create(
            {
                "name": "Stage 2",
                "action_id": cls.server_action_helpdesk_ticket.id,
                "sequence": 2,
            }
        )

    def test_helpdesk_ticket(self):
        self.helpdesk_ticket = self.HelpdeskTicket.create(
            {
                "name": "Helpdesk Ticket",
                "stage_id": self.helpdesk_ticket_stage_1.id,
                "description": "Helpdesk Ticket Description",
            }
        )
        self.helpdesk_ticket.write({"stage_id": self.helpdesk_ticket_stage_2.id})
        self.assertEqual(self.helpdesk_ticket.user_id, self.env.user)
