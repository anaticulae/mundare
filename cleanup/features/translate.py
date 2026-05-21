# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utilo

import cleanup.translate.lines


def work(
    text: str,
    text_baml: str,
    oneline_text: str,
    oneline_text_baml: str,
    prefix: str = '',
    pages: tuple = None,
) -> str:
    if prefix == 'oneline':
        text = determine_translation(
            src=oneline_text_baml,
            dst=oneline_text,
            pages=pages,
        )
    else:
        text = determine_translation(
            src=text_baml,
            dst=text,
            pages=pages,
        )
    return text


def determine_translation(src, dst, pages: tuple = None) -> str:
    if not utilo.exists(src):
        utilo.error(f'missing src: {src}')
        return utilo.NO_RESULT
    if not utilo.exists(dst):
        utilo.error(f'missing dst: {dst}')
        return utilo.NO_RESULT
    text_before = serializeraw.load_document(src, pages=pages)
    text = serializeraw.load_document(dst, pages=pages)
    text_translated = cleanup.translate.lines.translates(
        sources=text_before,
        destinations=text,
    )
    dumped = serializeraw.dump_translations(text_translated)
    return dumped
