# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def prepare(source, pages, td):
    utila.run(f'rawmaker -i {source} -o {td.tmpdir} --pages={pages} '
              '--text --fonts --images')
    utila.run(f'figureo -i {source} '
              f'-i {td.tmpdir} -o {td.tmpdir} --pages={pages}')
