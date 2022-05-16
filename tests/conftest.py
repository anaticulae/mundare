# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import cleanup

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = cleanup.PROCESS
WORKER = 6

power.setup(cleanup.ROOT)

RESOURCES = [
    (power.DISS205_PDF, '130:140'),
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR056_PDF,
    power.DISS143_PDF,
    power.HOME040_PDF,
]


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        pdfinfo=False,
        groupme=True,
        codero=True,
        pages=':',
        worker=WORKER,
        base=power.REPOSITORY,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
