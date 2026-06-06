# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import pytest
import serializeraw
import texmex
import utilo
import utilotest

import mundare.features.backup
import tests


def test_run_mundare(mp):
    tests.run('--help', mp=mp)


@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_bachelor56(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR056_PDF)
    utilo.copy_content(
        source,
        td.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
        unlock=True,
    )
    tests.run(
        '-i . -o . --cleanup --postfix=cleaned --pages=0',
        mp=mp,
    )
    assert len(utilo.file_list(td.tmpdir)) == 8


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR051_PDF)
def test_figures(td, mp):
    """Remove text in figure area."""
    source = hoverpower.link(hoverpower.BACHELOR051_PDF)
    tests.run(
        f'-i {source} -o {td.tmpdir}',
        mp=mp,
    )
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(td.tmpdir)
    assert ptn_dumped != ptn
    before = utilo.select_page(ptn, page=29)
    clean = utilo.select_page(ptn_dumped, page=29)
    # remove 4 lines on page 29
    assert len(clean) + 4 <= len(before)


@pytest.mark.xfail(reason='require footnote')
@utilotest.longrun
@utilotest.requires(hoverpower.MASTER193_PDF)
def test_footnotes(td, mp):
    """Remove text in footnotes area."""
    source = hoverpower.link(hoverpower.MASTER193_PDF)
    utilo.run(f'footnote -i {source} -o {td.tmpdir}')
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


@utilotest.requires(hoverpower.BACHELOR051_PDF)
def test_tables(td, mp):
    """Verify multiple input sources and tablero mundare."""
    source = hoverpower.link(hoverpower.BACHELOR051_PDF)
    page = 25
    # create table to verify removing table content
    tables = [
        iamraw.PageContentTableBounding(
            page=page,
            content=[iamraw.TableBounding(bounding=(0, 0, 300, 300))],
        )
    ]
    dumped = serializeraw.dump_tables(tables)
    utilo.file_create('tablero__decide_decide.yaml', dumped)
    # run mundare
    tests.run(
        f'-i {source} -i {td.tmpdir} -o {td.tmpdir} --pages={page}',
        mp=mp,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(td.tmpdir)
    assert ptn_dumped != ptn
    before = utilo.select_page(ptn, page=page)
    clean = utilo.select_page(ptn_dumped, page=page)
    # remove some lines due tablero
    assert len(before) == 55
    assert len(clean) < len(before)


@pytest.mark.xfail(reason='require formulero')
@utilotest.longrun
@utilotest.requires(hoverpower.DISS143_PDF)
def test_formulas(td, mp):
    source = hoverpower.link(hoverpower.DISS143_PDF)
    outdir = td.tmpdir
    page = 27
    utilo.run(
        f'formulero -i {hoverpower.DISS143_PDF} -o {outdir} --pages={page}')
    # run mundare
    tests.run(
        f'-i {source} -i {td.tmpdir} -o {outdir} --pages={page}',
        mp=mp,
    )
    # load result
    ptn = serializeraw.ptn_frompath(source)
    ptn_dumped = serializeraw.ptn_frompath(td.tmpdir)
    assert ptn_dumped != ptn
    before = utilo.select_page(ptn, page=page)
    clean = utilo.select_page(ptn_dumped, page=page)
    # remove some lines due formulero
    assert len(before) == 38
    assert len(clean) in {30, 31}


@utilotest.requires(hoverpower.BACHELOR051_PDF)
def test_backup(td, mp):
    """Copy source files as backup files(change data type)."""
    source = hoverpower.link(hoverpower.BACHELOR051_PDF)
    tests.run(
        f'-i {source} -o {td.tmpdir} --backup',
        mp=mp,
    )
    # four backup files written
    backupfiles = utilo.file_list(
        td.tmpdir,
        include=mundare.features.backup.BACKUP_EXT,
    )
    assert len(backupfiles) == 6
