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


def before(testdir):
    source = power.link(power.BACHELOR090_PDF)
    utila.copy_content(
        src=source,
        dst=testdir.tmpdir,
        unlock=True,
    )
    ensure_gap(testdir)


def ensure_gap(testdir):
    utila.cache_clear()
    ptn = serializeraw.ptn_frompath(
        testdir.tmpdir,
        fill_empty=False,
    )
    pages = [page.page for page in ptn]
    assert 14 in pages
    for page in utila.rtuple(15, 20):
        assert page not in pages, f'{page}: {pages}'
    assert 20 in pages


@utilatest.requires(power.BACHELOR090_PDF)
def test_bachelor90_withgap(testdir, mp):
    before(testdir)
    tests.run(f'-i {testdir.tmpdir} -o {testdir.tmpdir}', mp=mp)
    ensure_gap(testdir)
