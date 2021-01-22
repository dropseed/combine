# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_title_empty_check 1'] = [
    {
        'context': {
        },
        'type': 'title-empty'
    }
]

snapshots['test_title_missing_check 1'] = [
    {
        'context': {
        },
        'type': 'title-missing'
    }
]

snapshots['test_title_ok_check 1'] = [
]
