# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import iamraw
import texmex
import utilo

import mundare.load
import mundare.part.invalid
import mundare.ptn
import mundare.writer.result


def cleaner(  # pylint:disable=R0914
    inpaths: list,
    outpath: str,
    config: bool = None,
    prefix: str = '',
    postfix: str = '',
    pages=None,
):
    if not inpaths:
        inpaths = [os.getcwd()]
    if not outpath:
        outpath = inpaths[0]
    ptns = mundare.load.ptn_frompath(inpaths, prefix, pages)
    horizontals, lines = mundare.load.lines_frompath(
        inpaths,
        prefix,
        pages,
    )
    images = mundare.load.load_images(
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
        config=config,
    )
    fontstore = mundare.load.fontstore_frompath(inpaths, prefix, pages)
    document, textpositions, fontheader, fontcontent = mundare.ptn.dump_ptn(
        ptns,
        fontstore,
    )
    mundare.writer.result.write(
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
    config: dict = None,
    pages: tuple = None,
):
    invalids, noimages = mundare.part.invalid.create(
        inpaths,
        prefix,
        pages=pages,
        ptns=ptns,
        **config,
    )
    horizontals = mundare_horizontals(horizontals, invalids)
    lines = mundare_lines(lines, invalids)
    images = mundare_images(images, noimages)
    todo = [item.name.lower() for item in texmex.TextState]
    todo = [item for item in todo if item not in 'hidden visible']
    for element in todo:
        if config and not config.get(element, False):
            utilo.debug(f'do not remove: {element}')
            continue
        replacement = texmex.TextState[element.upper()]
        invalids = mundare.part.invalid.create(
            inpaths=inpaths,
            prefix=prefix,
            pages=pages,
            ptns=ptns,
            **{element: True},
        )[0]
        ptns = mundare_ptn(
            ptns,
            invalids,
            default=replacement,
        )
    return ptns, horizontals, lines, images


def mundare_ptn(
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
            if line.state != texmex.TextState.VISIBLE:
                utilo.verbose(f'do not overwrite state: {line} with {default}')
                continue
            line.state_change(default)
    return ptns


def mundare_horizontals(horizontals, invalids):
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


def mundare_lines(lines, invalids):
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


def mundare_images(images, invalids):
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


OVERLAPPING_RATE_MIN = configos.HV_PERCENT_PLUS(default=90)


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
        overlapping_rate = utilo.rect_overlapping(invalid, bounding)
        if overlapping_rate >= overlapping_min:
            return False
    return True
