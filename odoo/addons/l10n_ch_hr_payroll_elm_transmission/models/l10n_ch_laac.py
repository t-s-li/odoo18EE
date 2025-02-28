# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _

import string

class l10nChAdditionalAccidentInsurance(models.Model):
    _inherit = "l10n.ch.additional.accident.insurance"

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    insurance_company = fields.Char(required=False, store=True)
    active = fields.Boolean(default=True)


class l10nChAdditionalAccidentInsuranceLine(models.Model):
    _inherit = 'l10n.ch.additional.accident.insurance.line'

    solution_type = fields.Selection(
        selection_add=[(char, char) for char in string.ascii_uppercase[string.ascii_uppercase.index('C'):]] + [(str(num), str(num)) for num in range(10)],
        ondelete={code: 'set default' for code in 'CDEFGHIJKLMNOPQRSTUVXYWZ0123456789'},
        default="A")

    solution_number = fields.Selection(
        selection_add=[(char, char) for char in string.ascii_uppercase[string.ascii_uppercase.index('A'):]] + [(str(num), str(num)) for num in range(4, 10)],
        ondelete={code: 'set default' for code in 'ABCDEFGHIJKLMNOPQRSTUVXYWZ456789'},
        default="A")

    solution_code = fields.Char(compute="_compute_solution_code")

    @api.depends('solution_type', 'solution_number')
    def _compute_solution_code(self):
        for line in self:
            line.solution_code = line.solution_type + line.solution_number
