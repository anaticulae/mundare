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
def test_translate_lines(testdir):
    source, pages = power.BACHELOR037_PDF, '22,23,24'
    tests.utils.prepare(source, pages, testdir)
    # do not cache load_documents, do not use tests.run
    utila.run('cleanup --cleanup --backup '
              f'-i {testdir.tmpdir} -o {testdir.tmpdir}')
    ptn = serializeraw.ptn_frompath(testdir.tmpdir)
    backup = serializeraw.ptn_frompath(testdir.tmpdir, backup=True)
    assert ptn != backup, 'cached load_documents? check backup=False'
    translated = cleanup.translate.lines.translates(backup, ptn)
    # changes on two pages, no change on page 22
    assert len(translated) == 2


@utilatest.longrun
def test_cleanup_translate(testdir, monkeypatch):
    source, pages = power.BACHELOR037_PDF, '22,23,24'
    tests.utils.prepare(source, pages, testdir)
    tests.run(
        f'-i {testdir.tmpdir} -o {testdir.tmpdir}',
        monkeypatch=monkeypatch,
    )
    done = utila.file_list(
        testdir.tmpdir,
        recursive=False,
    )
    assert len(done) == 8
