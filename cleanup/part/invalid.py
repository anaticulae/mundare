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


def create(inpaths, prefix, pages: tuple = None):
    pagenumbers = cleanup.load.pagenumber_frompath(inpaths, pages)
    codes = cleanup.load.codes_frompath(inpaths, prefix, pages)
    formulas = cleanup.load.formulas_frompath(inpaths, prefix, pages)
    captions = cleanup.load.captions_frompath(inpaths, prefix, pages)
    images, tables = cleanup.load.load_images_tables(
        inpaths,
        pages=pages,
    )
    invalids = create_invalid_area(
        pagenumbers,
        images,
        tables,
        codes,
        formulas,
        captions,
    )
    noimages = create_invalid_area(
        pagenumbers=pagenumbers,
        images=[],
        tables=tables,
        codes=codes,
        formulas=formulas,
        captions=captions,
    )
    return invalids, noimages


def create_invalid_area(
    pagenumbers,
    images,
    tables,
    codes,
    formulas,
    captions,
) -> dict:
    invalid = collections.defaultdict(list)
    for number in pagenumbers:
        invalid[number.pdfpage].append(tuple(number.bounding))
    for page in images:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in tables:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in codes:
        tokens = utila.flatten([item.tokens_bounding for item in page.content])
        invalid[page.page].extend(tokens)
        # caption = utila.flatten([it.caption_bounding for it in page.content])
        # invalid[page.page].extend(caption)
    for page in formulas:
        invalid[page.page].extend([item.bounding for item in page.content])
    for page in captions:
        invalid[page.page].extend([item.bounding for item in page.content])
    # reduce rectangle count
    result = {
        key: utila.rectangle_merge(value) for key, value in invalid.items()
    }
    return result
