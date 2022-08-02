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
import utila
import utilatest

import cleanup.translate.lines
import tests
import tests.utils


@utilatest.longrun
@utilatest.requires(power.BACHELOR037_PDF)
def test_translate_lines(td):
    source, pages = power.BACHELOR037_PDF, '22,23,24'
    tests.utils.prepare(source, pages, td)
    # do not cache load_documents, do not use tests.run
    utila.run(f'cleanup --cleanup --backup -i {td.tmpdir} -o {td.tmpdir}')
    ptn = serializeraw.ptn_frompath(td.tmpdir)
    backup = serializeraw.ptn_frompath(td.tmpdir, backup=True)
    assert ptn != backup, 'cached load_documents? check backup=False'
    translated = cleanup.translate.lines.translates(backup, ptn)
    # changes on two pages, no change on page 22
    assert len(translated) == 2


@utilatest.longrun
@utilatest.requires(power.BACHELOR037_PDF)
def test_translate(td, mp):
    source, pages = power.BACHELOR037_PDF, '22,23,24'
    tests.utils.prepare(source, pages, td)
    tests.run(
        f'-i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    done = utila.file_list(
        td.tmpdir,
        recursive=False,
    )
    assert len(done) == 8
