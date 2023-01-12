# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import cleanup

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = cleanup.PROCESS

power.setup(cleanup.ROOT)

RESOURCES = [
    (power.BACHELOR090_PDF, '0:15,20:30'),
    (power.DISS172_PDF, '100:140'),
    (power.DISS205_PDF, '130:140'),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER116_PDF, '15:25'),
    (power.MASTER193_PDF, '0:30'),
    power.BACHELOR026_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR051_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR063_PDF,
    power.DISS143_PDF,
    power.HC_DISS128,
    power.HOME007_PDF,
    power.HOME043_PDF,
]

WORKER = utilatest.worker_count(4, onci=len(RESOURCES))


def extract(resources):
    genex.extract(
        files=resources,
        codero=True,
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        pdfinfo=False,
        tablero=True,
        worker=WORKER,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
