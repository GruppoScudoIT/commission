from . import models
from . import wizards

from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)
_logger.info("CARLO TOSOB")

table_renames = [
    ("sale_commission", "commission"),
    ("sale_commission_settlement", "commission_settlement"),
    ("sale_commission_make_invoice", "commission_make_invoice"),
    ("sale_commission_settlement_line", "commission_settlement_line"),
    ("sale_commission_make_settle", "commission_make_settle"),
]
model_renames = [
    ("sale.commission", "commission"),
    ("sale.commission.mixin", "commission.mixin"),
    ("sale.commission.line.mixin", "commission.line.mixin"),
    ("sale.commission.settlement", "commission.settlement"),
    ("sale.commission.make.invoice", "commission.make.invoice"),
    ("sale.commission.settlement.line", "commission.settlement.line"),
    ("sale.commission.make.settle", "commission.make.settle"),
]


def _handle_settlement_line_commission_id(cr):
    """On the new version, this field is computed stored, but the compute method
    doesn't resolve correctly the link here (as it's handled in `account_commission`),
    so we pre-create the column and fill it properly according old expected data.
    """
    openupgrade.logged_query(
        cr, "ALTER TABLE commission_settlement_line ADD commission_id int4"
    )
    openupgrade.logged_query(
        cr,
        """
        UPDATE commission_settlement_line csl
        SET commission_id = aila.commission_id
        FROM settlement_agent_line_rel rel
        JOIN account_invoice_line_agent aila ON aila.id = rel.agent_line_id
        WHERE rel.settlement_id = csl.id
        AND csl.commission_id IS NULL
        """,
    )

def _pre_init_test(cr):
    _logger.info("CARLO TOSOB1")

    openupgrade.rename_tables(cr, table_renames)
    openupgrade.rename_models(cr, model_renames)
    _handle_settlement_line_commission_id(cr)

def _post_init_test(cr, registry):
    """Convert the former `agent_line` m2m relation in `commission.line.mixin` into
    the new `settlement_line_ids` o2m relation."""
    _logger.info("CARLO TOSOB2")
    # openupgrade.logged_query(
    #     cr,
    #     """
    #         UPDATE commission_settlement_line
    #         SET invoice_agent_line_id = sal_rel.agent_line_id
    #         FROM (
    #             SELECT DISTINCT ON (agent_line_id) agent_line_id, settlement_id
    #             FROM settlement_agent_line_rel
    #             ORDER BY agent_line_id
    #         ) AS sal_rel
    #         WHERE id = sal_rel.settlement_id
    #     """,
    # )
    # All the existing settlements are of this type for now
    openupgrade.logged_query(
        cr,
        """
        UPDATE commission_settlement
        SET settlement_type = 'sale_invoice'
        """,
    )