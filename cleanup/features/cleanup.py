# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import cleanup.part.main


def work(  # pylint:disable=R0913
    select: str,
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
        image=not no_image,
        pagenumber=not no_pagenumber,
        table=not no_table,
    )
    config = config_select(
        config,
        select=select,
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
    return utilo.NO_RESULT


VALIDS = utilo.splititems("""\
caption code footnote formula headnote image pagenumber table
""")


def config_select(config: dict, select: str) -> dict:
    select = select.lower().strip()
    if select == 'all':
        return config
    config = {item: True for item in select.split()}
    if any(item not in VALIDS for item in config.keys()):
        utilo.exitx(msg=f'invalid selection: {config}')
    return config
