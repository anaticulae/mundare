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

import tests.utils


@pytest.mark.xfail(reason='software integration')
@utilotest.requires(hoverpower.DISS205_PDF)
def test_diss205p139(td, mp):
    """Ensure that code example is hidden correctly."""
    source, page = hoverpower.link(hoverpower.DISS205_PDF), 139
    utilo.copy_content(
        source,
        td.tmpdir,
        unlock=True,
    )
    tests.run(f'--pages {page} -o {td.tmpdir}', mp=mp)
    tests.cache_clear()
    ptn = serializeraw.ptcn_frompath(td.tmpdir)[0]
    assert ptn[0].text.startswith('Algorithmus 7.3:')
    assert ptn[1].text.startswith('Lösung bei der Minimierung')
    assert ptn[2].text.startswith('Als weitere Einstellung')
