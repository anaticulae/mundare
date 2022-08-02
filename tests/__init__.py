# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utilatest

import cleanup

run, failure = utilatest.create_cli_runner(cleanup)  #pylint: disable=invalid-name


def cache_clear():
    serializeraw.load_document.cache_clear()
    serializeraw.load_textpositions.cache_clear()
    serializeraw.load_horizontals.cache_clear()
