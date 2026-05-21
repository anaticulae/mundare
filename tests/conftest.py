# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import cleanup

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = cleanup.PROCESS

hoverpower.setup(cleanup.ROOT)

RESOURCES = [
    (hoverpower.BACHELOR090_PDF, '0:15,20:30'),
    (hoverpower.DISS172_PDF, '100:140'),
    (hoverpower.DISS205_PDF, '130:140'),
    (hoverpower.MASTER072_PDF, '0:10'),
    (hoverpower.MASTER116_PDF, '15:25'),
    (hoverpower.MASTER193_PDF, '0:30'),
    hoverpower.BACHELOR026_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR056_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.DISS143_PDF,
    hoverpower.HC_DISS128,
    hoverpower.HOME007_PDF,
    hoverpower.HOME043_PDF,
]

WORKER = utilotest.worker_count(4, onci=len(RESOURCES))


def extract(resources):
    gennex.extract(
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
    hoverpower.run()
