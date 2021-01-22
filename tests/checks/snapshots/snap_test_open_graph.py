# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_open_graph_image_check 1'] = [
    {
        'context': {
            'content': '/page'
        },
        'type': 'open-graph-image-not-canonical-https'
    }
]

snapshots['test_open_graph_missing_checks 1'] = [
    {
        'context': {
        },
        'type': 'open-graph-title-missing'
    }
]

snapshots['test_open_graph_missing_checks 2'] = [
    {
        'context': {
        },
        'type': 'open-graph-description-missing'
    }
]

snapshots['test_open_graph_missing_checks 3'] = [
    {
        'context': {
        },
        'type': 'open-graph-type-missing'
    }
]

snapshots['test_open_graph_missing_checks 4'] = [
    {
        'context': {
        },
        'type': 'open-graph-url-missing'
    }
]

snapshots['test_open_graph_missing_checks 5'] = [
    {
        'context': {
        },
        'type': 'open-graph-image-missing'
    }
]

snapshots['test_open_graph_missing_checks 6'] = [
    {
        'context': {
        },
        'type': 'open-graph-site-name-missing'
    }
]

snapshots['test_open_graph_url_check 1'] = [
    {
        'context': {
            'content': '/page'
        },
        'type': 'open-graph-url-not-canonical-https'
    }
]
