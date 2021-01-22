# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_meta_description_empty_check 1'] = [
    {
        'context': {
            'element': '<meta name="description"/>'
        },
        'type': 'meta-description-empty'
    }
]

snapshots['test_meta_description_length_check 1'] = [
    {
        'context': {
            'description': 'Whoops',
            'length': 6
        },
        'type': 'meta-description-length'
    }
]
