# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_img_alt_check 1'] = [
    {
        'context': {
            'element': '<img/>'
        },
        'type': 'image-alt-missing'
    }
]
