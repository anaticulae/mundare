# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Translater: Lines
=================

Translate navigator/lines between equal layout parser configuration.
The src navigator contains more lines then the dest navigator. These
lines where completly removed.

Example
-------

src      dest       translation
0        0(0)       1d->3s
1        -          2d->4s
2        -
3        3(1)
4        4(2)
"""

import texmex
import utila


def translates(sources, destinations) -> texmex.Translations:
    result = []
    for src, dest in utila.sync_pages((sources, destinations), numbers=False):
        if src is None or dest is None:
            # could not compute diff for empty page
            continue
        if not src and not dest:
            # translation is not required, cause pages are empty
            continue
        assert src.page == dest.page, f'{src.page} == {dest.page}'
        # sync pages to avoid asyncs with empty pages
        translated = translate(src, dest)
        if not translated:
            continue
        table = texmex.Translation(page=src.page)
        for now, before in translated:
            # TODO: IMPROVE BAD NAMING
            table.add(now, before)
        result.append(table)
    return result


def translate(
    src: texmex.PTN,
    dest: texmex.PTN,
) -> list:
    """\
    >>> translate(('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'D'))
    []
    >>> translate(('A', 'B', 'C', 'D', 'E'), ('A', 'C', 'D'))
    [(1, 2), (2, 3)]

    Dest contains item which are not part of source navigator
    >>> translate(('A', 'B', 'C', 'D', 'E'), ('A', 'C', 'D', 'F', 'G'))
    Traceback (most recent call last):
    ...
    ValueError: src and dest does not match. Could not match index: **3** width data: **F**

    >>> translate((), ('A',))
    Traceback (most recent call last):
        ...
    ValueError: source is empty: () | ('A',)
    """
    if not src:
        raise ValueError(f'source is empty: {src} | {dest}')
    result = []
    left = 0
    vdest = [item for item in dest if isinstance(item, str) or item.visible]
    for right, dest_item in enumerate(vdest):
        collected = find(src, start=left, search=dest_item)
        if collected == -1:
            if hasattr(src, 'page'):
                utila.error(f'page: {src.page}')
                utila.error('SOURCE')
                for item in src:
                    utila.error(f'{hash(str(item))}:   {str(item).strip()}')
                utila.error('=======================')
                utila.error('DEST')
                for item in vdest:
                    utila.error(f'{hash(str(item))}:   {str(item).strip()}')
            error = ('src and dest does not match. Could not match index: '
                     f'**{right}** width data: **{dest_item}**')
            raise ValueError(error)
        if not result and collected == right:
            left = collected + 1
            continue
        result.append((right, collected))
        left = collected + 1
    return result


def find(container, start, search):
    # TODO: COMPARISON ON LINUX DOES NOT WORK, STR DOES.
    search = hash(str(search))
    for index, item in enumerate(container[start:], start=start):
        item = hash(str(item))
        if search == item:
            return index
    return -1
