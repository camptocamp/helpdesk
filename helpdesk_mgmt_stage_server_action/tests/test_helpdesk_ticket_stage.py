# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import RecordCapturer, TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class HelpdeskTicketStageServerAction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.HelpdeskTicket = cls.env["helpdesk.ticket"]
        cls.HelpdeskTicketStage = cls.env["helpdesk.ticket.stage"]
        cls.HelpdeskTicketTag = cls.env["helpdesk.ticket.tag"]
        cls.ServerAction = cls.env["ir.actions.server"]
        cls.create_tag_action = cls.env["ir.actions.server"].create(
            {
                "model_id": cls.env["ir.model"]._get_id("helpdesk.ticket.tag"),
                "crud_model_id": cls.env["ir.model"]._get_id("helpdesk.ticket.tag"),
                "name": "Create new helpdesk tag",
                "value": "New helpdesk tag",
                "state": "object_create",
            }
        )
        cls.stage_1 = cls.HelpdeskTicketStage.create(
            {"name": "Stage 1", "sequence": 1, "action_id": cls.create_tag_action.id}
        )
        cls.ticket = cls.HelpdeskTicket.create(
            {
                "name": "Create a tag ticket",
                "description": "Ticket Description",
            }
        )

    def test_helpdesk_ticket_run_action(self):
        self.assertFalse(
            self.HelpdeskTicketTag.search([("name", "=", "New helpdesk tag")]).exists()
        )
        with RecordCapturer(self.HelpdeskTicketTag, []) as capture:
            self.ticket.write({"stage_id": self.stage_1.id})
        tag = capture.records
        self.assertEqual(1, len(tag))
        self.assertEqual("New helpdesk tag", tag.name)
