# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import mundare

DESCRIPTION = """\
Load PTNs, codes, figures and tables.

It removes text which is inside codes, figures and or tables and writes
PTNs afterwards.

Select mundare All: [caption code footnote formula headnote image pagenumber table]
"""

WORKPLAN = [
    utilo.create_step('backup'),
    utilo.create_step(
        'mundare',
        inputs=[
            utilo.Value('select', str, defaultvar='all'),
            utilo.Value('postfix', str, defaultvar=''),
            utilo.Bool('no_caption'),
            utilo.Bool('no_code'),
            utilo.Bool('no_footnote'),
            utilo.Bool('no_formula'),
            utilo.Bool('no_headnote'),
            utilo.Bool('no_image'),
            utilo.Bool('no_pagenumber'),
            utilo.Bool('no_table'),
        ],
    ),
    utilo.create_step(
        'translate',
        inputs=[
            utilo.ResultFile(
                producer='rawmaker',
                name='text_text',
                optional=True,
            ),
            utilo.ResultFile(
                producer='rawmaker',
                name='text_text',
                ext='baml',
                optional=True,
            ),
            utilo.ResultFile(
                producer='rawmaker',
                name='oneline_text_text',
                optional=True,
            ),
            utilo.ResultFile(
                producer='rawmaker',
                name='oneline_text_text',
                ext='baml',
                optional=True,
            ),
        ],
        output=('text',),
    ),
]


@utilo.saveme
def main():
    utilo.featurepack(
        root=mundare.ROOT,
        workplan=WORKPLAN,
        featurepackage='mundare.features',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=False,
            name=mundare.PROCESS,
            pages=True,
            version=mundare.__version__,
        ),
    )
