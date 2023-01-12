# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

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
            source=oneline_text_baml,
            dest=oneline_text,
            pages=pages,
        )
    else:
        text = determine_translation(
            source=text_baml,
            dest=text,
            pages=pages,
        )
    return text


def determine_translation(source, dest, pages: tuple = None) -> str:
    if not utila.exists(source):
        utila.error(f'missing source: {source}')
        return utila.NO_RESULT
    if not utila.exists(dest):
        utila.error(f'missing dest: {dest}')
        return utila.NO_RESULT
    text_before = serializeraw.load_document(source, pages=pages)
    text = serializeraw.load_document(dest, pages=pages)
    text_translated = cleanup.translate.lines.translates(
        sources=text_before,
        destinations=text,
    )
    dumped = serializeraw.dump_translations(text_translated)
    return dumped
