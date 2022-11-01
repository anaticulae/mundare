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
import tests.conftest


@utilatest.nightly
@pytest.mark.parametrize(
    'source',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
def test_pagenumber_remove_x(source, td, mp):
    """Hide detected page number to improve footnote extraction result."""
    source = power.link(source)
    pattern = '(rawmaker__text|rawmaker__fonts|pagenumber__result)_*.yaml'
    utila.copy_content(
        source,
        td.tmpdir,
        pattern=pattern,
        unlock=True,
    )
    pagenumbers = serializeraw.load_pagenumbers(td.tmpdir)
    pdfpages = set(item.pdfpage for item in pagenumbers)  # pylint:disable=E1101
    assert pdfpages
    befores = serializeraw.ptn_frompath(td.tmpdir)
    tests.run(f'--select=pagenumber -i {td.tmpdir} -o {td.tmpdir}', mp=mp)
    # clear cache to load filtered data
    tests.cache_clear()
    afters = serializeraw.ptn_frompath(td.tmpdir)
    for before, after in zip(befores, afters):
        assert before.page == after.page
        expected = len(before)
        if before.page in pdfpages:
            expected -= 1
        assert len(after) == expected
