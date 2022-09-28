# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import cleanup.load
import tests


@utilatest.requires(power.DISS172_PDF)
def test_horizontals_diss172p138(td, mp):
    """Remove horizontals which are part of a detected table."""
    source, page = power.link(power.DISS172_PDF), 138
    utila.copy_content(
        source,
        td.tmpdir,
        unlock=True,
    )
    before = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=cleanup.load.HORIZONTALS_WIDTH_MIN,
        pages=page,
    )
    tests.run(
        f'--pages {page} -i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    tests.cache_clear()
    after = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=cleanup.load.HORIZONTALS_WIDTH_MIN,
        pages=page,
    )
    assert after != before


@utilatest.longrun
@utilatest.requires(power.MASTER193_PDF)
def test_horizontals_master193(td, mp):
    source = power.link(power.MASTER193_PDF)
    utila.copy_content(
        source,
        td.tmpdir,
        unlock=True,
    )
    before = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=cleanup.load.HORIZONTALS_WIDTH_MIN,
    )
    tests.run(
        f'-i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    tests.cache_clear()
    after = serializeraw.load_horizontals(
        td.tmpdir,
        width_min=cleanup.load.HORIZONTALS_WIDTH_MIN,
    )
    # page 25 is deleted cause horizontal as underline in footer is
    # removed by new footnote skipper.
    before = [item for item in before if item.page != 25]
    after = [item for item in after if item.page != 25]
    assert after == before
