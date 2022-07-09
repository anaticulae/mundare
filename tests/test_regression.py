# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests.utils


def test_translate_diss143page25(td, mp):
    """Regression test to ensure that all lines are matched together.

    LEFT:           RIGHT
    1. A             1. A
       B             2. B
       C             3. C
    2. DEF           4. D
    3. GHF           5. E

    Before changing to single line, it was not possible to determine
    transformation: 2. B -> 1. B
    """
    source = power.DISS143_PDF
    # fails before
    raw = translate(source, 25, td, mp)
    assert raw


def test_master116p18table(td, mp):
    """Do not remove very near caption line in table."""
    source = power.MASTER116_PDF
    raw = translate(source, 18, td, mp)
    # ensure that caption line in table is not cleaned
    assert 'Tab. 2.1.: Übersicht Hybridlokomotiven [Kon13]' in raw


def translate(source, page: int, td, mp) -> str:
    utilatest.fixture_requires(source)
    tests.utils.prepare(source, page, td)
    tests.run('', monkeypatch=mp)
    serializeraw.load_document.cache_clear()
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
    raw = ptn.debug
    return raw
