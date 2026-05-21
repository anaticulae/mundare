# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utilo

import cleanup.writer.image


def write(
    outpath: str,
    document: iamraw.Document,
    textpositions: iamraw.TextPositions,
    fontheader: dict,
    fontcontent: list,
    horizontals: list,
    lines: list,
    images: list,
    prefix: str = '',
    postfix: str = '',
):
    prefix = prefix or ''
    postfix = postfix or ''
    # write document
    utilo.file_replace(
        iamraw.path.text(outpath, prefix=prefix + postfix),
        document,
    )
    utilo.file_replace(
        iamraw.path.textposition(outpath, prefix=prefix + postfix),
        textpositions,
    )
    if fontheader is not None and fontcontent is not None:
        # write reduced font store
        utilo.file_replace(
            iamraw.path.fontheader(outpath, prefix=prefix + postfix),
            fontheader,
        )
        utilo.file_replace(
            iamraw.path.fontcontent(outpath, prefix=prefix + postfix),
            fontcontent,
        )
    cleanup.writer.image.write(outpath, images)
    # write lines
    if horizontals is not None:
        # None signals that the source does not contain any horizontal file
        utilo.file_replace(
            iamraw.path.horizontals(outpath, prefix=postfix),
            serializeraw.dump_horizontals(horizontals),
        )
    if lines is not None:
        # None signals that the source does not contain any line file
        utilo.file_replace(
            iamraw.path.line(outpath, prefix=postfix),
            serializeraw.dump_lines(lines),
        )
