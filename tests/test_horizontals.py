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


@utilatest.requires(power.DISS172_PDF)
def test_horizontals_diss172p138(testdir, monkeypatch):
    """Remove horizontals which are part of a detected table."""
    source, page = power.link(power.DISS172_PDF), 138
    utila.copy_content(
        source,
        testdir.tmpdir,
        unlock=True,
    )
    before = serializeraw.load_horizontals(testdir.tmpdir, pages=page)
    tests.run(
        f'--pages {page} -i {testdir.tmpdir} -o {testdir.tmpdir}',
        monkeypatch=monkeypatch,
    )
    serializeraw.load_horizontals.cache_clear()
    after = serializeraw.load_horizontals(testdir.tmpdir, pages=page)
    assert after != before
