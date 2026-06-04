# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import texmex
import utilotest

import tests


@pytest.mark.xfail(reason='require footnote')
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_footnotes_master072(td, mp):
    source = hoverpower.link(hoverpower.MASTER072_PDF)
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
