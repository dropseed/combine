# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_duplicate_id_check 1'] = [
    {
        'context': {
            'element': '<img src="http://example.com/image.png"/>'
        },
        'type': 'https-mixed-content'
    },
    {
        'context': {
            'element': '<link href="http://another.com/style.css" rel="stylesheet"/>'
        },
        'type': 'https-mixed-content'
    },
    {
        'context': {
            'element': '''<iframe src="http://external.com">
</iframe>'''
        },
        'type': 'https-mixed-content'
    }
]
