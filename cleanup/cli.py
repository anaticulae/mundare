# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import cleanup

DESCRIPTION = """\
Load PTNs, codes, figures and tables.

It removes text which is inside codes, figures and or tables and writes
PTNs afterwards.

Select cleanup All: [caption code footnote formula headnote image pagenumber table]
"""

WORKPLAN = [
    utila.create_step('backup'),
    utila.create_step(
        'cleanup',
        inputs=[
            utila.Value('select', str, defaultvar='all'),
            utila.Value('postfix', str, defaultvar=''),
            utila.Bool('no_caption'),
            utila.Bool('no_code'),
            utila.Bool('no_footnote'),
            utila.Bool('no_formula'),
            utila.Bool('no_headnote'),
            utila.Bool('no_image'),
            utila.Bool('no_pagenumber'),
            utila.Bool('no_table'),
        ],
    ),
    utila.create_step(
        'translate',
        inputs=[
            utila.ResultFile(
                producer='rawmaker',
                name='text_text',
                optional=True,
            ),
            utila.ResultFile(
                producer='rawmaker',
                name='text_text',
                ext='baml',
                optional=True,
            ),
            utila.ResultFile(
                producer='rawmaker',
                name='oneline_text_text',
                optional=True,
            ),
            utila.ResultFile(
                producer='rawmaker',
                name='oneline_text_text',
                ext='baml',
                optional=True,
            ),
        ],
        output=('text',),
    ),
]


@utila.saveme
def main():
    utila.featurepack(
        root=cleanup.ROOT,
        workplan=WORKPLAN,
        featurepackage='cleanup.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=False,
            name=cleanup.PROCESS,
            pages=True,
            version=cleanup.__version__,
        ),
    )
