# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilo
import utilotest

import tests


def before(td):
    source = hoverpower.link(hoverpower.BACHELOR090_PDF)
    utilo.copy_content(
        src=source,
        dst=td.tmpdir,
        unlock=True,
    )
    ensure_gap(td)


def ensure_gap(td):
    utilo.cache_clear()
    ptn = serializeraw.ptn_frompath(
        td.tmpdir,
        fill_empty=False,
    )
    pages = [page.page for page in ptn]
    assert 14 in pages
    for page in utilo.rtuple(15, 20):
        assert page not in pages, f'{page}: {pages}'
    assert 20 in pages


@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_bachelor90_withgap(td, mp):
    before(td)
    tests.run(f'-i {td.tmpdir} -o {td.tmpdir}', mp=mp)
    ensure_gap(td)
