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
import utila
import utilatest

import tests


@utilatest.longrun
def test_headnotes(td, mp):
    source = power.link(power.BACHELOR037_PDF)
    utila.run(f'headnote -i {source} -o {td.tmpdir}')
    tests.run(
        f'-i {source} -i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    headnote_only = serializeraw.ptn_frompath(
        td.tmpdir,
        state=texmex.TextState.HEADNOTE,
    )
    content = [item for item in headnote_only if item]
    assert content, 'could not load headnote-state-content'
