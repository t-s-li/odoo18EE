# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests.common import tagged
from odoo.tools import file_open
import json
from unittest.mock import patch


_logger = logging.getLogger(__name__)


@tagged('post_install_l10n', 'post_install', '-at_install', 'swissdec')
class TestSwissdecCommon(AccountTestInvoicingCommon):

    @classmethod
    @AccountTestInvoicingCommon.setup_country('ch')
    def setUpClass(cls):
        super().setUpClass()
        cls.maxDiff = None
        with patch.object(cls.env.registry['l10n.ch.employee.yearly.values'], '_generate_certificate_uuid', lambda self: "#DOC-ID"):
            mapped_declarations = cls.env.company._l10n_ch_generate_swissdec_demo_data()

        for indentifier, declaration in mapped_declarations.items():
            assert isinstance(indentifier, str)
            setattr(cls, indentifier, declaration)

    def _normalize_data(self, data):
        """
        Recursively transform data so that the order of lists no longer matters.
        """
        if isinstance(data, dict):
            return {k: self._normalize_data(v) for k, v in sorted(data.items(), key=lambda d: str(d))}
        elif isinstance(data, list):
            return sorted([self._normalize_data(item) for item in data], key=lambda d: str(d))
        else:
            return data

    def _compare_with_truth_base(self, declaration_type, identifier, generated_dict):
        truth_base = json.load(file_open(f'test_l10n_ch_hr_payroll_account/data/declaration_truth_base/{declaration_type}.json')),
        truth_dict = truth_base[0].get(identifier)

        json_formated = json.loads(json.dumps(generated_dict))

        self.assertDictEqual(
            self._normalize_data(json_formated),
            self._normalize_data(truth_dict),
            f"Mismatch in declaration '{identifier}'."
        )