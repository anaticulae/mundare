# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import utilo

import cleanup.load


def create(
    inpaths,
    prefix,
    pages: tuple = None,
    ptns: list = None,
    **kwargs: dict,
):
    pagenumbers, codes, formulas, captions, images, tables, footnotes, headnotes =\
        ([], [], [], [], [], [], [], [])
    if kwargs.get('pagenumber', False):
        pagenumbers = cleanup.load.pagenumber_frompath(inpaths, pages)
    if kwargs.get('code', False):
        codes = cleanup.load.codes_frompath(inpaths, prefix, pages)
    if kwargs.get('formula', False):
        formulas = cleanup.load.formulas_frompath(inpaths, prefix, pages)
    if kwargs.get('caption', False):
        captions = cleanup.load.captions_frompath(inpaths, prefix, pages)
    if kwargs.get('image', False):
        images = cleanup.load.load_images(inpaths, pages=pages)
    if kwargs.get('table', False):
        tables = cleanup.load.load_tables(inpaths, pages=pages)
    if kwargs.get('footnote', False):
        footnotes = cleanup.load.footnotes_frompath(inpaths, pages=pages)
    if kwargs.get('headnote', False):
        headnotes = cleanup.load.headnotes_frompath(inpaths, pages=pages)
    invalids = create_invalid_area(
        captions=captions,
        codes=codes,
        footnotes=footnotes,
        formulas=formulas,
        headnotes=headnotes,
        images=images,
        pagenumbers=pagenumbers,
        tables=tables,
        ptns=ptns,
    )
    noimages = create_invalid_area(
        captions=captions,
        codes=codes,
        footnotes=footnotes,
        formulas=formulas,
        headnotes=headnotes,
        images=[],
        pagenumbers=pagenumbers,
        tables=tables,
        ptns=ptns,
    )
    return invalids, noimages


def create_invalid_area(  # pylint:disable=R0914
    captions,
    codes,
    footnotes,
    formulas,
    headnotes,
    images,
    pagenumbers,
    tables,
    ptns,
) -> dict:
    invalid = collections.defaultdict(list)
    for number in pagenumbers:
        invalid[number.pdfpage].append(tuple(number.bounding))
    invalid.update(create_footnotes(footnotes))
    invalid.update(create_header_footer(headnotes, ptns))
    for data in (
            images,
            tables,
            formulas,
            captions,
    ):
        for page in data:
            invalid[page.page].extend([item.bounding for item in page.content])
    for page in codes:
        tokens = utilo.flat([item.tokens_bounding for item in page.content])
        invalid[page.page].extend(tokens)
        # caption = utilo.flat([it.caption_bounding for it in page.content])
        # invalid[page.page].extend(caption)
    # reduce rectangle count
    result = {key: utilo.rect_merge(value) for key, value in invalid.items()}
    return result


def create_header_footer(headnotes, ptns) -> dict:
    invalid = collections.defaultdict(list)
    for headnote in headnotes:
        ptn = utilo.select_page(ptns, page=headnote.page)
        if not ptn:
            continue
        pagewidth, pageheight = ptn.width, ptn.height
        if headnote.header:
            invalid[headnote.page].append((
                0.0,
                0.0,
                pagewidth,
                headnote.header.end * pageheight,
            ))
            if refs := headnote.header.refs:
                for ref in refs:
                    invalid[headnote.page].append(ref)
        if headnote.footer:
            invalid[headnote.page].append((
                0.0,
                headnote.footer.begin * pageheight,
                pagewidth,
                headnote.footer.end * pageheight,
            ))
            if refs := headnote.footer.refs:
                for ref in refs:
                    invalid[headnote.page].append(ref)
    return invalid


def create_footnotes(footnotes) -> dict:
    invalid = collections.defaultdict(list)
    for page in footnotes:
        for footnote in page.content:
            bbox = footnote.bounding
            if not bbox:
                utilo.error(f'missing footnote bounding: {footnote}')
                continue
            # increase bounding to match footnotes correctly.
            # left and right is no problem, cause in gernal there is
            # nothing when we handle normal footnotes
            # bottom is also not a problem
            # top is a problem, we do not want to hide any normal text content
            scale = (0.8, 1.0, 1.3, 1.05)
            bbox = utilo.rect_scale(bbox, scale=scale)
            invalid[page.page].append(bbox)
    return invalid
