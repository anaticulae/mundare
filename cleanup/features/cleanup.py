# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import cleanup.part.main


def work(  # pylint:disable=R0913
    postfix: str,
    no_caption: bool = False,
    no_code: bool = False,
    no_footnote: bool = False,
    no_formula: bool = False,
    no_headnote: bool = False,
    no_image: bool = False,
    no_pagenumber: bool = False,
    no_table: bool = False,
    inputs: str = None,
    outputs: str = None,
    prefix: str = '',
    pages: tuple = None,
):
    # figure is important, do not rename, see TextState
    config = dict(
        caption=not no_caption,
        code=not no_code,
        footnote=not no_footnote,
        formula=not no_formula,
        headnote=not no_headnote,
        figure=not no_image,
        pagenumber=not no_pagenumber,
        table=not no_table,
    )
    # POSTFIX as value first!
    cleanup.part.main.cleaner(
        inpaths=inputs,
        outpath=outputs,
        config=config,
        prefix=prefix,
        postfix=postfix,
        pages=pages,
    )
    return utila.NO_RESULT
