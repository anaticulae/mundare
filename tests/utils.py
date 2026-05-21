# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo


def prepare(source, pages, td):
    utilo.run(f'rawmaker -i {source} -o {td.tmpdir} --pages={pages} '
              '--text --fonts --images')
    utilo.run(f'figureo -i {source} '
              f'-i {td.tmpdir} -o {td.tmpdir} --pages={pages}')
