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

import tests


def test_pagenumber_remove_diss143(td, mp):
    source = power.link(power.DISS143_PDF)
    pattern = '(rawmaker__text|rawmaker__fonts|pagenumber__result)_*.yaml'
    utila.copy_content(
        source,
        td.tmpdir,
        pattern=pattern,
        unlock=True,
    )
    pagenumbers = serializeraw.load_pagenumbers(td.tmpdir)
    pdfpages = set(item.pdfpage for item in pagenumbers)
    befores = serializeraw.ptn_frompath(td.tmpdir)
    tests.run(f'-i {td.tmpdir} -o {td.tmpdir}', mp=mp)
    # clear cache to load filtered data
    serializeraw.load_document.cache_clear()
    serializeraw.load_textpositions.cache_clear()
    afters = serializeraw.ptn_frompath(td.tmpdir)
    for before, after in zip(befores, afters):
        assert before.page == after.page
        expected = len(before)
        if before.page in pdfpages:
            expected -= 1
        assert len(after) == expected
