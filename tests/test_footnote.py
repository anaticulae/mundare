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
import texmex
import utilatest

import tests


@utilatest.requires(power.MASTER072_PDF)
def test_footnotes_master072(td, mp):
    source = power.link(power.MASTER072_PDF)
    tests.run(
        f'-i {source}  -o {td.tmpdir}',
        mp=mp,
    )
    footer_only = serializeraw.ptn_frompath(
        td.tmpdir,
        state=texmex.TextState.FOOTNOTE,
        pages=(8,),
    )[0]
    assert len(footer_only) == 4, '4 footnotes'
