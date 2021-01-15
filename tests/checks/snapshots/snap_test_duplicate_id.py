# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_duplicate_id_check 1'] = [
    {
        'context': {
            'elements': [
                '<img id="foo" src="https://example.com/image.png"/>',
                '<div id="foo"></div>'
            ],
            'id': 'foo'
        },
        'type': 'duplicate-id'
    }
]
