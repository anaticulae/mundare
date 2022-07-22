# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import iamraw
import texmex
import utila

import cleanup.load
import cleanup.part.invalid
import cleanup.ptn
import cleanup.writer.result


def cleaner(  # pylint:disable=R0914
    inpaths: list,
    outpath: str,
    prefix: str = '',
    postfix: str = '',
    pages=None,
):
    if not inpaths:
        inpaths = [os.getcwd()]
    if not outpath:
        outpath = inpaths[0]
    ptns = cleanup.load.ptn_frompath(inpaths, prefix, pages)
    horizontals, lines = cleanup.load.lines_frompath(
        inpaths,
        prefix,
        pages,
    )
    images = cleanup.load.load_images(
        inpaths,
        pages,
    )
    # remove content here
    ptns, horizontals, lines, images = remove_skip_area(
        ptns,
        horizontals,
        lines,
        images=images,
        inpaths=inpaths,
        prefix=prefix,
        pages=pages,
    )
    fontstore = cleanup.load.fontstore_frompath(inpaths, prefix, pages)
    document, textpositions, fontheader, fontcontent = cleanup.ptn.dump_ptn(
        ptns,
        fontstore,
    )
    cleanup.writer.result.write(
        outpath,
        document,
        textpositions,
        fontheader,
        fontcontent,
        horizontals,
        lines,
        images=images,
        prefix=prefix,
        postfix=postfix,
    )


def remove_skip_area(
    ptns,
    horizontals,
    lines,
    images,
    inpaths: list,
    prefix,
    pages: tuple = None,
):
    invalids, noimages = cleanup.part.invalid.create(
        inpaths,
        prefix,
        pages,
        captions=True,
        codes=True,
        formulas=True,
        images=True,
        pagenumbers=True,
        tables=True,
    )
    ptns = cleanup_ptn(ptns, invalids)
    horizontals = cleanup_horizontals(horizontals, invalids)
    lines = cleanup_lines(lines, invalids)
    images = cleanup_images(images, noimages)
    return ptns, horizontals, lines, images


def cleanup_ptn(
    ptns,
    invalids,
    default=texmex.TextState.HIDDEN,
):
    for ptn in ptns:
        if ptn.page not in invalids:
            # no invalid possible
            continue
        # line intersects with invalid area
        invalid_lines = [
            item for item in ptn
            if not valid_bounding(item.bounding, invalids, ptn.page)
        ]
        for line in invalid_lines:
            line.state_change(default)
    return ptns


def cleanup_horizontals(horizontals, invalids):
    if not horizontals:
        return horizontals
    horizontals = [
        iamraw.PageContentHorizontals(
            page=page.page,
            content=[
                item
                for item in page.content
                if valid_bounding(item.box, invalids, page.page)
            ])
        for page in horizontals
    ]
    return horizontals


def cleanup_lines(lines, invalids):
    if not lines:
        return lines
    lines = [
        iamraw.PageContentLine(
            page=page.page,
            content=[
                item
                for item in page.content
                if valid_bounding(item, invalids, page.page)
            ],
        )
        for page in lines
    ]
    return lines


def cleanup_images(images, invalids):
    """Skip images which are overlapped by table, formula, code or
    something else.

    We prefare these extraction over image extraction.
    """
    if not images:
        return images
    for page in images:
        for image in page.content:
            if valid_bounding(image.bounding, invalids, page.page):
                continue
            # image is overlapped by table, formula, code or something,
            # skip image
            image.hidden = True
    return images


OVERLAPPING_RATE_MIN = configo.HV_PERCENT_PLUS(default=90)


def valid_bounding(
    bounding: tuple,
    invalids: dict,
    page: int,
    overlapping_min: float = OVERLAPPING_RATE_MIN,
) -> bool:
    try:
        invalid_area = invalids[page]
    except KeyError:
        return True
    for invalid in invalid_area:
        overlapping_rate = utila.rect_overlapping(invalid, bounding)
        if overlapping_rate >= overlapping_min:
            return False
    return True
