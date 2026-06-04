# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import serializeraw
import utilo


def write(outpath, images):
    if not images:
        return
    baseimage = iamraw.path.images(outpath)
    os.makedirs(baseimage, exist_ok=True)
    for page in images:
        for image in page.content:
            if not image.hidden:
                continue
            imagepath = utilo.join(baseimage, f'{image.hashedimage}.yaml')
            dumped = serializeraw.dump_image_info(image)
            utilo.file_replace(imagepath, dumped)
