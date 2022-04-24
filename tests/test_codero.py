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

import tests.utils


def test_diss205p139(testdir, monkeypatch):
    """Ensure that code example is hidden correctly."""
    source, page = power.link(power.DISS205_PDF), 139
    utila.copy_content(
        source,
        testdir.tmpdir,
    )
    tests.run(f'--pages {page} -o {testdir.tmpdir}', monkeypatch=monkeypatch)
    serializeraw.load_document.cache_clear()
    ptn = serializeraw.ptcn_frompath(testdir.tmpdir)[0]
    assert ptn[0].text.startswith('Algorithmus 7.3:')
    assert ptn[1].text.startswith('Lösung bei der Minimierung')
    assert ptn[2].text.startswith('Als weitere Einstellung')
