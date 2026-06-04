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
import texmex
import utilo
import utilotest

import tests


@pytest.mark.xfail(reason='require headnote')
@pytest.mark.parametrize('source', (
    pytest.param(hoverpower.BACHELOR026_PDF, id='bachelor026'),
    pytest.param(hoverpower.BACHELOR037_PDF, id='bachelor037'),
))
@utilotest.longrun
def test_headnotes_ensure_load(source, td, mp):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    utilo.run(f'headnote -i {source} -o {td.tmpdir}')
    tests.run(
        f'-i {source} -i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    headnote_only = serializeraw.ptn_frompath(
        td.tmpdir,
        state=texmex.TextState.HEADNOTE,
    )
    content = [item for item in headnote_only if item]
    assert content, 'could not load headnote-state-content'


@pytest.mark.xfail(reason='headnote')
@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR063_PDF)
def test_headnotes_bachelor063(td, mp):
    source = hoverpower.BACHELOR063_PDF
    source = hoverpower.link(source)
    utilo.run(f'headnote -i {source} -o {td.tmpdir}')
    tests.run(f'-i {source} -i {td.tmpdir} -o {td.tmpdir}', mp=mp)
    headnote_only = serializeraw.ptn_frompath(
        td.tmpdir,
        state=texmex.TextState.HEADNOTE,
    )
    content = [item for item in headnote_only if item]
    assert content, 'could not load headnote-state-content'


@pytest.mark.xfail(reason='require headnote')
@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR063_PDF)
def test_bachelor063_cleanup_horizontals(td, mp):
    """Use header.refs to remove horizontals."""
    source, pages = hoverpower.BACHELOR063_PDF, '--pages=0:10'
    source = hoverpower.link(source)
    before = serializeraw.load_horizontals(source, pages=(2,))
    utilo.run(f'headnote -i {source} -o {td.tmpdir} {pages}')
    tests.run(f'-i {source} -i {td.tmpdir} -o {td.tmpdir} {pages}', mp=mp)
    after = serializeraw.load_horizontals(td.tmpdir, pages=(2,))
    assert after != before
    assert len(before[0].content) == 3
    # remove headnote and footnote
    assert len(after[0].content) == 1
