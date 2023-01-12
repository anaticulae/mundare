# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import texmex
import utila
import utilatest

import cleanup.features.backup
import tests


def test_run_cleanup(mp):
    tests.run('--help', mp=mp)


@utilatest.requires(power.BACHELOR056_PDF)
def test_bachelor56(td, mp):
    source = power.link(power.BACHELOR056_PDF)
    utila.copy_content(
        source,
        td.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
        unlock=True,
    )
    tests.run(
        '-i . -o . --cleanup --postfix=cleaned --pages=0',
        mp=mp,
    )
    assert len(utila.file_list(td.tmpdir)) == 8


@utilatest.longrun
@utilatest.requires(power.BACHELOR051_PDF)
def test_figures(td, mp):
    """Remove text in figure area."""
    source = power.link(power.BACHELOR051_PDF)
    tests.run(
        f'-i {source} -o {td.tmpdir}',
        mp=mp,
    )
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(td.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=29)
    clean = utila.select_page(ptn_dumped, page=29)
    # remove 4 lines on page 29
    assert len(clean) + 4 <= len(before)


@utilatest.longrun
@utilatest.requires(power.MASTER193_PDF)
def test_footnotes(td, mp):
    """Remove text in footnotes area."""
    source = power.link(power.MASTER193_PDF)
    utila.run(f'footnote -i {source} -o {td.tmpdir}')
    tests.run(
        f'-i {source} -i {td.tmpdir} -o {td.tmpdir}',
        mp=mp,
    )
    footnote_only = serializeraw.ptn_frompath(
        td.tmpdir,
        state=texmex.TextState.FOOTNOTE,
    )
    content = [item for item in footnote_only if item]
    assert content, 'could not load footnote-state-content'


@utilatest.requires(power.BACHELOR051_PDF)
def test_tables(td, mp):
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
        f'-i {source} -i {td.tmpdir} -o {td.tmpdir} --pages={page}',
        mp=mp,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(td.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=page)
    clean = utila.select_page(ptn_dumped, page=page)
    # remove some lines due tablero
    assert len(before) == 55
    assert len(clean) < len(before)


@utilatest.longrun
@utilatest.requires(power.DISS143_PDF)
def test_formulas(td, mp):
    source = power.link(power.DISS143_PDF)
    outdir = td.tmpdir
    page = 27
    utila.run(f'formulero -i {power.DISS143_PDF} -o {outdir} --pages={page}')
    # run cleanup
    tests.run(
        f'-i {source} -i {td.tmpdir} -o {outdir} --pages={page}',
        mp=mp,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(td.tmpdir)
    assert ptn_dumped != ptn
    before = utila.select_page(ptn, page=page)
    clean = utila.select_page(ptn_dumped, page=page)
    # remove some lines due formulero
    assert len(before) == 38
    assert len(clean) in {30, 31}


@utilatest.requires(power.BACHELOR051_PDF)
def test_backup(td, mp):
    """Copy source files as backup files(change data type)."""
    source = power.link(power.BACHELOR051_PDF)
    tests.run(
        f'-i {source} -o {td.tmpdir} --backup',
        mp=mp,
    )
    # four backup files written
    backupfiles = utila.file_list(
        td.tmpdir,
        include=cleanup.features.backup.BACKUP_EXT,
    )
    assert len(backupfiles) == 6
