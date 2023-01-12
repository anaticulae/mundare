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

import tests


def before(td):
    source = power.link(power.BACHELOR090_PDF)
    utila.copy_content(
        src=source,
        dst=td.tmpdir,
        unlock=True,
    )
    ensure_gap(td)


def ensure_gap(td):
    utila.cache_clear()
    ptn = serializeraw.ptn_frompath(
        td.tmpdir,
        fill_empty=False,
    )
    pages = [page.page for page in ptn]
    assert 14 in pages
    for page in utila.rtuple(15, 20):
        assert page not in pages, f'{page}: {pages}'
    assert 20 in pages


@utilatest.requires(power.BACHELOR090_PDF)
def test_bachelor90_withgap(td, mp):
    before(td)
    tests.run(f'-i {td.tmpdir} -o {td.tmpdir}', mp=mp)
    ensure_gap(td)
