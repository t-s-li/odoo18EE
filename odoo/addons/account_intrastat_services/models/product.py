# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_valid_intrastat_code_ids(self, valid_intrastat_codes):
        self.ensure_one()
        if 'service' in valid_intrastat_codes and self.type == 'service':
            return valid_intrastat_codes['service']
        return super()._get_valid_intrastat_code_ids(valid_intrastat_codes)
