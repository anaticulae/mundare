# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import utila

import cleanup.load


def create(inpaths, prefix, pages: tuple = None, **kwargs: dict):
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
    if kwargs.get('figure', False):
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
    )
    return invalids, noimages


def create_invalid_area(
    captions,
    codes,
    footnotes,
    formulas,
    headnotes,
    images,
    pagenumbers,
    tables,
) -> dict:
    invalid = collections.defaultdict(list)
    for number in pagenumbers:
        invalid[number.pdfpage].append(tuple(number.bounding))
    for page in footnotes:
        for footnote in page.content:
            if not footnote.bounding:
                utila.error(f'missing footnote bounding: {footnote}')
                continue
            invalid[page.page].append(tuple(footnote.bounding))
    for data in (
            images,
            tables,
            formulas,
            captions,
    ):
        for page in data:
            invalid[page.page].extend([item.bounding for item in page.content])
    for page in codes:
        tokens = utila.flatten([item.tokens_bounding for item in page.content])
        invalid[page.page].extend(tokens)
        # caption = utila.flatten([it.caption_bounding for it in page.content])
        # invalid[page.page].extend(caption)
    # reduce rectangle count
    result = {
        key: utila.rectangle_merge(value) for key, value in invalid.items()
    }
    return result
