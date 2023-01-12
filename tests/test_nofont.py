# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests


@utilatest.longrun
@utilatest.requires(power.BACHELOR056_PDF)
def test_no_fontstore_bachelor56(td, mp):
    """Run cleanup without any font information.

    Ensure that no fontstore file is generated.
    """
    source = power.link(power.BACHELOR056_PDF)
    utila.copy_content(
        source,
        td.tmpdir,
        pattern='rawmaker__text_*.yaml',
        unlock=True,
    )
    tests.run('-i . -o .', mp=mp)
    # 5=> text, textpos and two backups, cleanup_translate and no fontstore
    assert len(utila.file_list(td.tmpdir)) == 5
