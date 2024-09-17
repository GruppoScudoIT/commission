from . import models
from . import wizards
from . import report

from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)


def _post_init_test(cr, registry):
    """Fill new invoice_agent_line_id many2one from the old many2many agent_line
    equivalent table. This table always contain only one record on standard use.
    """
    _logger.info("CARLO TOSOB3")
    openupgrade.logged_query(
        cr,
        """
        UPDATE commission_settlement_line csl
        SET invoice_agent_line_id = agent_line_id
        FROM settlement_agent_line_rel rel
        WHERE rel.settlement_id = csl.id
        """,
    )
