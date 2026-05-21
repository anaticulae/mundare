# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilo
import utilotest

import cleanup.translate.lines
import tests
import tests.utils


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR037_PDF)
def test_translate_lines(td):
    source, pages = hoverpower.BACHELOR037_PDF, '22,23,24'
    tests.utils.prepare(source, pages, td)
    # do not cache load_documents, do not use tests.run
    utilo.run(f'cleanup --cleanup --backup -i {td.tmpdir} -o {td.tmpdir}')
    ptn = serializeraw.ptn_frompath(td.tmpdir)
    backup = serializeraw.ptn_frompath(td.tmpdir, backup=True)
    assert ptn != backup, 'cached load_documents? check backup=False'
    translated = cleanup.translate.lines.translates(backup, ptn)
    # changes on two pages, no change on page 22
    assert len(translated) == 2


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR037_PDF)
def test_translate(td, mp):
    source, pages = hoverpower.BACHELOR037_PDF, '22,23,24'
    tests.utils.prepare(source, pages, td)
    tests.run(
        f'-i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    done = utilo.file_list(
        td.tmpdir,
        recursive=False,
    )
    assert len(done) == 8
