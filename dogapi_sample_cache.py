"""
Shared sample data for the Dog API (v2) homework unit tests.

This file exists so `sample_cache` doesn't need to be duplicated inside
both `new/solution.py` and `new/startercode.py`.
"""

# Real Dog API v2 group ids (these are UUID strings returned/used by the API)
import json
from linecache import cache


GROUP_ID_HOUND = 'be0147df-7755-4228-b132-2518c0c6d10d'  # e.g., the group used by Breed A/B
GROUP_ID_TOY = 'f56dc4b1-ba1a-4454-8ce2-bd5d41404a0c'  # e.g., the group used by Breed C
GROUP_ID_HERDING = 'b8e4e89d-057f-432a-9e58-0b85b29b693c'  # e.g., the group used by Breed D


# This is intentionally a "fake" cache dict used for testing pure logic.
# Its JSON shape matches the parts of Dog API v2 responses used by the
# homework functions:
#   - data.attributes.name
#   - data.attributes.life.max
#   - data.attributes.hypoallergenic
#   - data.relationships.group.data.id
SAMPLE_CACHE = {
    'https://dogapi.dog/api/v2/breeds/1': {
        'data': {
            'id': '1',
            'type': 'breed',
            'attributes': {
                'name': 'Breed A',
                'life': {'min': 10, 'max': 14},
                'hypoallergenic': True
            },
            'relationships': {
                'group': {
                    'data': {
                        'id': GROUP_ID_HOUND,
                        'type': 'group'
                    }
                }
            }
        }
    },
    'https://dogapi.dog/api/v2/breeds/2': {
        'data': {
            'id': '2',
            'type': 'breed',
            'attributes': {
                'name': 'Breed B',
                'life': {'min': 9, 'max': 12},
                'hypoallergenic': True
            },
            'relationships': {
                'group': {
                    'data': {
                        'id': GROUP_ID_HOUND,
                        'type': 'group'
                    }
                }
            }
        }
    },
    'https://dogapi.dog/api/v2/breeds/3': {
        'data': {
            'id': '3',
            'type': 'breed',
            'attributes': {
                'name': 'Breed C',
                'life': {'min': 12, 'max': 16},
                'hypoallergenic': False
            },
            'relationships': {
                'group': {
                    'data': {
                        'id': GROUP_ID_TOY,
                        'type': 'group'
                    }
                }
            }
        }
    },
    'https://dogapi.dog/api/v2/breeds/4': {
        'data': {
            'id': '4',
            'type': 'breed',
            'attributes': {
                'name': 'Breed D',
                'life': {'min': 11, 'max': 13},
                'hypoallergenic': False
            },
            'relationships': {
                'group': {
                    'data': {
                        'id': GROUP_ID_HERDING,
                        'type': 'group'
                    }
                }
            }
        }
    },
    'https://dogapi.dog/api/v2/breeds/5': {
        'data': {
            'id': '5',
            'type': 'breed',
            'attributes': {
                'name': 'Breed E',
                'life': {'min': 8, 'max': 10},
                'hypoallergenic': False
            }
            # No relationships.group.data for Breed E (used to test the error path)
        }
    }
}

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def create_cache(dictionary, filename):
    with open(filename, 'w') as f:
        json.dump(dictionary, f)

def search_breed(breed_id):
    url = f'https://dogapi.dog/api/v2/breeds/{breed_id}'
    cache = load_json('cache.json')
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json().get('data') is not None:
            cache[url] = response.json()
            cache[url]['status_code'] = response.status_code
            create_cache(cache, 'cache.json')
            return (response.json(), url)
        else:
            cache[url] = {'status_code': response.status_code, 'data': None}
            create_cache(cache, 'cache.json')
            return None
       