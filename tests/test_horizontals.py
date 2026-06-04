# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import mundare.load
import tests


@pytest.mark.xfail(reason='require tablero')
@utilotest.requires(hoverpower.DISS172_PDF)
def test_horizontals_diss172p138(td, mp):
    """Remove horizontals which are part of a detected table."""
    source, page = hoverpower.link(hoverpower.DISS172_PDF), 138
    utilo.copy_content(
        source,
        td.tmpdir,
        unlock=True,
    )
    before = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=mundare.load.HORIZONTALS_WIDTH_MIN,
        pages=page,
    )
    tests.run(
        f'--pages {page} -i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    tests.cache_clear()
    after = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=mundare.load.HORIZONTALS_WIDTH_MIN,
        pages=page,
    )
    assert after != before


@utilotest.longrun
@utilotest.requires(hoverpower.MASTER193_PDF)
def test_horizontals_master193(td, mp):
    source = hoverpower.link(hoverpower.MASTER193_PDF)
    utilo.copy_content(
        source,
        td.tmpdir,
        unlock=True,
    )
    before = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=mundare.load.HORIZONTALS_WIDTH_MIN,
    )
    tests.run(
        f'-i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    tests.cache_clear()
    after = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=mundare.load.HORIZONTALS_WIDTH_MIN,
    )
    # page 25 is deleted cause horizontal as underline in footer is
    # removed by new footnote skipper.
    before = [item for item in before if item.page != 25]
    after = [item for item in after if item.page != 25]
    assert after == before
