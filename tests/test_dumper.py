# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import tests


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.BACHELOR056_PDF, '0:10,20:25', id='partial'),
    pytest.param(power.BACHELOR056_PDF, '15', id='fifteen'),
    pytest.param(power.BACHELOR056_PDF, '27', id='27'),
    pytest.param(power.BACHELOR056_PDF, '5,6,7', id='fiveSixSeven'),
    pytest.param(power.DISS143_PDF, '27', id='diss143'),
])
def test_source_compare_reduction_fast(source, pages, td, mp):
    """Ensure that resource is loaded and dumped correctly.

    This is required before we can test that cleanup reduces some data
    out of ptn.
    """
    compare(source, pages, td, mp)


@utilatest.nightly
@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR037_PDF, id='bachelor037'),
    pytest.param(power.BACHELOR051_PDF, id='bachelor51'),
    pytest.param(power.BACHELOR056_PDF, id='bachelor56'),
    pytest.param(power.DISS143_PDF, id='diss143'),
    pytest.param(power.HC_DISS128, id='hcdiss128'),
    pytest.param(power.HOME040_PDF, id='home040'),
])
def test_source_compare_reduction_slow(source, td, mp):
    compare(source, ':', td, mp)


def compare(source, pages, td, mp):
    utilatest.fixture_requires(source)
    source = power.link(source)
    utila.copy_content(
        source,
        td.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
        unlock=True,
    )
    tests.run(
        f'-i {td.tmpdir} -o {td.tmpdir} --postfix=cleaned --pages={pages}',
        mp=mp,
    )
    pages = utila.parse_pages(pages)
    ptn = serializeraw.ptn_frompath(
        td.tmpdir,
        pages=pages,
    )
    ptn_dumped = serializeraw.ptn_frompath(
        td.tmpdir,
        prefix='cleaned',
        pages=pages,
    )
    assert ptn_dumped == ptn
    fontstore = serializeraw.fs_frompath(
        td.tmpdir,
        pages=pages,
    )
    fontstore_dumped = serializeraw.fs_frompath(
        td.tmpdir,
        prefix='cleaned',
        pages=pages,
    )
    assert fontstore_dumped.pages == fontstore.pages
    assert fontstore_dumped.header == fontstore.header
