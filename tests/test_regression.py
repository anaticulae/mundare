# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import tests
import tests.utils


@utilatest.longrun
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


@utilatest.longrun
def test_master116p18table(td, mp):
    """Do not remove very near caption line in table."""
    source = power.MASTER116_PDF
    raw = translate(source, 18, td, mp)
    # ensure that caption line in table is not cleaned
    assert 'Tab. 2.1.: Übersicht Hybridlokomotiven [Kon13]' in raw


def translate(source, page: int, td, mp) -> str:
    utilatest.fixture_requires(source)
    tests.utils.prepare(source, page, td)
    tests.run('', mp=mp)
    tests.cache_clear()
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
    raw = ptn.debug
    return raw


@utilatest.requires(power.HC_DISS128)
def test_hc_diss128_rawmaker_error(td, mp):
    """Negative font size produces an error while using rawmaker

    scale_fromchar(char).
    """
    source = power.link(power.HC_DISS128)
    if not utila.exists(source):
        pytest.skip(reason='generate HC_DISS128')
    pages = '32,45,62,83,97,98'
    tests.run(f'-i {source} -o {td.tmpdir} --pages {pages}', mp=mp)


@utilatest.longrun
@utilatest.requires(power.HOME007_PDF)
def test_run_cleanup_multiple_times(td, mp):
    """Ensure that hidden data is loaded before running cleanup step.

    If we do not load hidden data, this data gots lost if we run cleanup
    again. To access hidden data later, we have to load it on every
    cleanup step.

    See 2ac5651e78c02c5520d5d
    """
    source = power.link(power.HOME007_PDF)
    before = [len(page) for page in serializeraw.ptn_frompath(path=source)]
    tests.cache_clear()
    tests.run(
        f'-i {source} -o {td.tmpdir}',
        mp=mp,
    )
    tests.cache_clear()
    after = [len(page) for page in serializeraw.ptn_frompath(path=td.tmpdir)]
    assert after != before
    for _ in range(4):
        tests.run(f'-i {td.tmpdir} -o {td.tmpdir}', mp=mp)
        tests.cache_clear()
        current = [
            len(page) for page in serializeraw.ptn_frompath(path=td.tmpdir)
        ]
        assert current == after
