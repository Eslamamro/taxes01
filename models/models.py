# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class taxes01(models.Model):

    _name = 'taxes01.taxes01'
    _description = 'taxes01.taxes01'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone')
    state = fields.Char(string="State")
    Registered_E_invoicing = fields.Boolean(string="E-invoicing")
    is_2023 = fields.Boolean(string="2023")
    registration_number = fields.Char(string="Registration Number")
    date = fields.Date(string="Date")
    registration_company = fields.Char(string="Registration Company")
    token_pass = fields.Char(string="Token Pass")
    portal_request = fields.Selection(
        [
            ('active', 'Active'),
            ('not-active', 'Not-Active'),
            ('unknown_password', 'Unknown_Password'),
            ('waiting', 'Waiting'),
        ],
        string="Portal Request",
        required=False,
        default='not-active'
    )
    vat_checkbox = fields.Boolean(string="vat")
    username = fields.Char(string='Username')
    email = fields.Char(string='Email1')
    password = fields.Char(string='Password1', required=False, help="Password for the user")
    password2 = fields.Char(string='Password2', required=False, help="Password for the user")
    tag_ids = fields.Many2many('task.tag', string="Tags")
    tax_id = fields.Char(string='Tax ID')
    
    def action_redirect_to_taxes(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://auth.eta.gov.eg:8080/auth/realms/e-tax/protocol/openid-connect/auth?client_id=etax-sso&redirect_uri=https%3A%2F%2Fwww.eta.gov.eg%2Far%2Fhome&state=5a044569-c907-4ead-8789-da2bc139bf8f&response_mode=fragment&response_type=code&scope=openid&nonce=f137ea73-1bb2-47f1-81af-2f1cab601825',  # Redirects to Facebook
            'target': 'new',  # Opens in the same tab/window
        }

    def action_redirect_to_invoices(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://eservice.incometax.gov.eg/etax',  # Redirects to Facebook
            'target': 'new',  # Opens in the same tab/window
        }

    def action_redirect_to_E_invoicing(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://id.eta.gov.eg/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3D9A029E3B-7403-4B25-8850-AB67E1FD92AB%26redirect_uri%3Dhttps%253A%252F%252Finvoicing.eta.gov.eg%252Flogin%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520publicportals.bff.api%26state%3D0f031ae44f874b9bbb7bd17aa36ce8bb%26nonce%3Dde53ae8c43be41c89a8832176e8b53d5',  # Redirects to Facebook
            'target': 'new',  # Opens in the same tab/window
        }

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



class Task(models.Model):
    _name = 'task.task'
    _description = 'Task'
    _inherit = ['taxes01.taxes01', 'mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(
        'taxes01.taxes01',
        string='Name')
    date = fields.Date(string='Date')
    notes = fields.Html(string='Notes')
    upload = fields.Binary()
    income = fields.Many2one('taxes01.income', string='Income')

    last_check = fields.Many2one(
        'last.check',
        string='Last check')

    vat = fields.Many2one('taxes01.vat', string='vat')
    phone = fields.Char(string='Phone')
    tax_id = fields.Char(string='Tax ID')
    due_date = fields.Date(string="Due Date", required=True, default=lambda self: fields.Date.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Status', default='draft', track_visibility='onchange', required=True)

    def mark_done(self):
        """Mark the task as 'Done' and remove associated activities."""
        for task in self:
            # Update the task's state to "Done"
            task.write({'state': 'done'})

            # Search for activities linked to this task and unlink them
            activities = self.env['mail.activity'].search([
                ('res_model', '=', 'task.task'),
                ('res_id', '=', task.id)
            ])
            activities.sudo().unlink()  # Remove associated activities from the chatter
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',  # Reload the form view to reflect changes
        }

    def create_activity(self):
        """Creates a new activity and subscribes relevant partners to the task."""
        for task in self:
            if not task.due_date:
                raise ValidationError(_("The task must have a Due Date to create an activity."))

            # Get the activity type (To-Do)
            activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
            if not activity_type:
                raise ValidationError(_("The 'To-Do' activity type is missing. Please configure activity types."))

            # Fetch the Document Model (res_model_id)
            model_id = self.env['ir.model'].search([('model', '=', self._name)], limit=1)
            if not model_id:
                raise ValidationError(_("The model '%s' is not properly configured in Odoo.") % self._name)

            # Create the activity
            activity = self.env['mail.activity'].create({
                'res_model_id': model_id.id,  # Use the model's ID, not its name
                'res_id': task.id,  # Link to the specific task record
                'activity_type_id': activity_type.id,  # To-Do activity type
                'summary': f"Task State Update: {task.state}",  # Add task state to summary
                'date_deadline': task.due_date,  # Set activity deadline to task's due date

            })

            # Optionally, subscribe followers (if required)
            partner_ids = []  # Add partner IDs if needed
            if partner_ids:
                task.message_subscribe(partner_ids=partner_ids)

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',  # Reload the form view to reflect changes
            }

    @api.model
    def action_open_wizard_func(self):

        action = self.env['ir.actions.action']._for_xml_id('taxes01.action_task_wizard')
        return action


class Vat(models.Model):

    _name = 'taxes01.vat'
    _description = 'Vat'

    name = fields.Char(string='Name')

    @api.model
    def _create_default_records(self):
        """Create default records if they don't already exist."""
        default_records = [
            {'name': 'Yearly'},
            {'name': 'Monthly'},
            {'name': 'Quarter'},
        ]

        for default_record in default_records:
            if not self.search([('name', '=', default_record['name'])]):
                self.create(default_record)  # Create a single record at a time

    @api.model
    def init(self):
        """Automatically create default records when the module is installed."""
        self._create_default_records()


class Income(models.Model):

    _name = 'taxes01.income'
    _description = 'income'

    name = fields.Char(string='Name')

    @api.model
    def _create_default_records(self):
        """Create default records if they don't already exist."""
        default_records = [
            {'name': 'Yearly'},
            {'name': 'Monthly'},
            {'name': 'Quarter'},
        ]

        for default_record in default_records:
            if not self.search([('name', '=', default_record['name'])]):
                self.create(default_record)  # Create a single record at a time

    @api.model
    def init(self):
        """Automatically create default records when the module is installed."""
        self._create_default_records()


class LastCheck(models.Model):
    _name = 'last.check'

    name = fields.Char(string='Name')

    @api.model
    def _create_default_records(self):
        """Create default records if they don't already exist."""
        default_records = [
            {'name': 'Yearly'},
            {'name': 'Monthly'},
            {'name': 'Quarter'},
        ]

        for default_record in default_records:
            if not self.search([('name', '=', default_record['name'])]):
                self.create(default_record)  # Create a single record at a time

    @api.model
    def init(self):
        """Automatically create default records when the module is installed."""
        self._create_default_records()






class TaskTag(models.Model):
    _name = 'task.tag'
    _description = 'Task Tag'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")

    @api.model
    def _create_default_tags(self):
        """Create default tags with Odoo colors."""
        default_tags = [
            {'name': 'Urgent', 'color': 1},  # Red
            {'name': 'Important', 'color': 2},  # Green
            {'name': 'Low Priority', 'color': 3},  # Blue
            {'name': 'Review', 'color': 4},  # Yellow
        ]

        for tag in default_tags:
            if not self.search([('name', '=', tag['name'])]):
                self.create(tag)

    @api.model
    def init(self):
        """Automatically create default tags when the module is installed."""
        self._create_default_tags()


