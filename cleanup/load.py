# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import serializeraw
import utila

HORIZONTALS_WIDTH_MIN = configo.HV_INT_PLUS(default=50)

# If we do not load hidden and run cleanup multiple times, hidden data is
# lost and not accessible later.
LOAD_HIDDEN = None


def ptn_frompath(inpaths, prefix, pages):
    for inpath in inpaths:
        utila.debug(f'ptn: {inpath}')
        ptns = serializeraw.ptn_frompath(
            inpath,
            prefix=prefix,
            pages=pages,
            sort=False,
            state=LOAD_HIDDEN,
            fill_empty=False,
        )
        if ptns is not None:
            return ptns
    return None


def pagenumber_frompath(inpaths, pages):
    for inpath in inpaths:
        path = iamraw.path.pagenumber_result(inpath)
        if not utila.exists(path):
            continue
        utila.debug(f'pagenumber: {path}')
        loaded = serializeraw.load_pagenumbers(path, pages=pages)
        return loaded
    return []


def codes_frompath(inpaths, prefix, pages):  # pylint:disable=W0613
    result = []
    for inpath in inpaths:
        path = iamraw.path.codero_result(inpath)
        if not utila.exists(path):
            continue
        utila.debug(f'codes: {path}')
        loaded = serializeraw.load_codes(path, pages=pages)
        result.extend(loaded)
    return result


def formulas_frompath(inpaths, prefix, pages):  # pylint:disable=W0613
    result = []
    for inpath in inpaths:
        path = iamraw.path.formula(inpath)
        if not utila.exists(path):
            continue
        utila.debug(f'formulas: {path}')
        loaded = serializeraw.load_rawformulas(path, pages=pages)
        result.extend(loaded)
    return result


def captions_frompath(inpaths, prefix, pages):  # pylint:disable=W0613
    result = []
    for inpath in inpaths:
        path = iamraw.path.caption_result(inpath)
        if not utila.exists(path):
            continue
        utila.debug(f'formulas: {path}')
        loaded = serializeraw.load_captions(path, pages=pages)
        result.extend(loaded)
    return result


def footnotes_frompath(inpaths, pages):  # pylint:disable=W0613
    result = []
    for inpath in inpaths:
        path = iamraw.path.footnote_result(inpath)
        if not utila.exists(path):
            continue
        utila.debug(f'footnote: {path}')
        loaded = serializeraw.load_footnotes(path, pages=pages)
        result.extend(loaded)
    return result


def headnotes_frompath(inpaths, pages):  # pylint:disable=W0613
    result = []
    for inpath in inpaths:
        path = iamraw.path.headnote_result(inpath)
        if not utila.exists(path):
            continue
        utila.debug(f'headnote: {path}')
        loaded = serializeraw.load_headerfooter(path, pages=pages)
        result.extend(loaded)
    return result


def lines_frompath(inpaths: list, prefix: str, pages: tuple) -> tuple:
    """Load lines and horizontal lines from `inpaths`.

    Args:
        inpaths(list): list of possible sources
        prefix(str): prefix inpath data
        pages(tuple): selected pages
    Returns:
        Filtered horizontals and lines

    Hint: It is only required to write the result file if the source
    file exists. We have to destingush between non existing, empty
    source file and empty remove source file.
    It is enough to have two groups, we only want to know if we must
    write the empty file.
    """
    prefix = ''  # DISABLE PREFIX
    horizontals, lines = None, None
    for inpath in inpaths:
        utila.debug(f'lines: {inpath}')
        if utila.exists(iamraw.path.horizontals(inpath)):
            # if utila.exists(iamraw.path.horizontals(inpath, prefix)):
            # use list, to signal that line source file exists.
            horizontals = horizontals or []
            horizontals.extend(
                serializeraw.load_horizontals(
                    inpath,
                    prefix=prefix,
                    pages=pages,
                    width_min=HORIZONTALS_WIDTH_MIN,
                ))
        if utila.exists(iamraw.path.line(inpath)):
            # if utila.exists(iamraw.path.line(inpath, prefix)):
            # use list, to signal that line source file exists.
            lines = lines or []
            lines.extend(
                serializeraw.load_lines(
                    inpath,
                    prefix=prefix,
                    pages=pages,
                ))
    if horizontals:
        for pdfpage in horizontals:
            utila.verbose(
                f'p{pdfpage.page} horizontal: {len(pdfpage.content)}',
                end=' ',
            )
    if lines:
        for pdfpage in lines:
            utila.verbose(
                f'p{pdfpage.page} lines: {len(pdfpage.content)}',
                end=' ',
            )
    return horizontals, lines


def fontstore_frompath(inpaths, prefix, pages):
    for inpath in inpaths:
        utila.debug(f'fontstore: {inpath}')
        fontstore = serializeraw.fs_frompath(
            inpath,
            prefix=prefix,
            pages=pages,
        )
        if fontstore:
            return fontstore
    return None


def load_images(inpaths: list, pages: tuple = None):
    result = []
    # load images and tables from multiple `inpaths`
    for inpath in inpaths:
        imagepath = iamraw.path.images(inpath)
        if not utila.exists(imagepath):
            continue
        result.extend(
            serializeraw.load_image_infos_frompath(
                imagepath,
                pages=pages,
            ))
    return result


def load_tables(inpaths: list, pages: tuple = None):
    result = []
    # load tables from multiple `inpaths`
    for inpath in inpaths:
        tableropath = iamraw.path.tablero_result(inpath)
        utila.debug(f'tablero: {tableropath}')
        if not utila.exists(tableropath):
            continue
        result.extend(serializeraw.load_tables(tableropath, pages=pages))
    return result
