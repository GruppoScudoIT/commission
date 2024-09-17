from . import models
from . import wizards
import logging

_logger = logging.getLogger(__name__)
_logger.info("CARLO TOSOB")

def _pre_init_test(cr):
    _logger.info("CARLO TOSOB1")
    table_renames = [
        ("sale_commission", "commission"),
        ("sale_commission_settlement", "commission_settlement"),
        ("sale_commission_make_invoice", "commission_make_invoice"),
        ("sale_commission_settlement_line", "commission_settlement_line"),
        ("sale_commission_make_settle", "commission_make_settle"),
    ]
    for old,new in table_renames:
        cr.execute(f"ALTER TABLE {old} RENAME TO {new};")
        
    cr.commit()
