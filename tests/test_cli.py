# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import cleanup.features.backup
import tests


def test_run_cleanup(monkeypatch):
    tests.run('--help', monkeypatch=monkeypatch)


@utilatest.requires(power.BACHELOR056_PDF)
def test_bachelor56(testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    utila.copy_content(
        source,
        testdir.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
    )
    tests.run(
        '-i . -o . --cleanup --postfix=cleaned --pages=0',
        monkeypatch=monkeypatch,
    )
    assert len(utila.file_list(testdir.tmpdir)) == 8


@utilatest.longrun
@utilatest.requires(power.BACHELOR051_PDF)
def test_figures(testdir, monkeypatch):
    """Remove text in figure area."""
    source = power.link(power.BACHELOR051_PDF)
    tests.run(
        f'-i {source} -o {testdir.tmpdir}',
        monkeypatch=monkeypatch,
    )
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(testdir.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=29)
    clean = utila.select_page(ptn_dumped, page=29)
    # remove 4 lines on page 29
    assert len(clean) + 4 == len(before)


@utilatest.requires(power.BACHELOR051_PDF)
def test_tables(testdir, monkeypatch):
    """Verify multiple input soruces and tablero cleanup."""
    source = power.link(power.BACHELOR051_PDF)
    page = 25
    # create table to verify removing table content
    tables = [
        iamraw.PageContentTableBounding(
            page=page,
            content=[iamraw.TableBounding(bounding=(0, 0, 300, 300))],
        )
    ]
    dumped = serializeraw.dump_tables(tables)
    utila.file_create('tablero__decide_decide.yaml', dumped)
    # run cleanup
    tests.run(
        f'-i {source} -i {testdir.tmpdir} -o {testdir.tmpdir} --pages={page}',
        monkeypatch=monkeypatch,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(testdir.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=page)
    clean = utila.select_page(ptn_dumped, page=page)
    # remove some lines due tablero
    assert len(before) == 55
    assert len(clean) < len(before)


@utilatest.longrun
@utilatest.requires(power.DISS143_PDF)
def test_formulas(testdir, monkeypatch):
    source = power.link(power.DISS143_PDF)
    outdir = testdir.tmpdir
    page = 27
    utila.run(f'formulero -i {power.DISS143_PDF} -o {outdir} --pages={page}')
    # run cleanup
    tests.run(
        f'-i {source} -i {testdir.tmpdir} -o {outdir} --pages={page}',
        monkeypatch=monkeypatch,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(testdir.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=page)
    clean = utila.select_page(ptn_dumped, page=page)
    # remove some lines due formulero
    assert len(before) == 38
    assert len(clean) == 31


@utilatest.requires(power.BACHELOR051_PDF)
def test_backup(testdir, monkeypatch):
    """Copy source files as backup files(change data type)."""
    source = power.link(power.BACHELOR051_PDF)
    tests.run(
        f'-i {source} -o {testdir.tmpdir} --backup',
        monkeypatch=monkeypatch,
    )
    # four backup files written
    backupfiles = utila.file_list(
        testdir.tmpdir,
        include=cleanup.features.backup.BACKUP_EXT,
    )
    assert len(backupfiles) == 6
