# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilo
import utilotest

import tests


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_no_fontstore_bachelor56(td, mp):
    """Run mundare without any font information.

    Ensure that no fontstore file is generated.
    """
    source = hoverpower.link(hoverpower.BACHELOR056_PDF)
    utilo.copy_content(
        source,
        td.tmpdir,
        pattern='rawmaker__text_*.yaml',
        unlock=True,
    )
    tests.run('-i . -o .', mp=mp)
    # 5=> text, textpos and two backups, mundare_translate and no fontstore
    assert len(utilo.file_list(td.tmpdir)) == 5
