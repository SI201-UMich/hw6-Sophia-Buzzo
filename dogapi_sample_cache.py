"""
Shared sample data for the Dog API (v2) homework unit tests.

This file exists so `sample_cache` doesn't need to be duplicated inside
both `new/solution.py` and `new/startercode.py`.
"""

# Real Dog API v2 group ids (these are UUID strings returned/used by the API)
import json
from linecache import cache
import requests


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
    except requests.exceptions. RequestsException:
        return None
    
def update_cache(breed_ids, cache_file):
    cache = load_json(cache_file)
    successful_caches = 0
    total_breeds = len(breed_ids)

    for breed in breed_ids:
        url = f'https://dogapi.dog/api/v2/breeds/{breed}'
        
        if url in cache and cache[url].get('status_code') == 200 and cache[url].get('data') is not None:
            continue
       
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json().get('data') is not None:
                cache[url] = response.json()
                cache[url]['status_code'] = response.status_code
                successful_caches += 1
        except requests.exceptions.RequestException:
            pass
    create_cache(cache, cache_file)
    if total_breeds > 0:
        percentage = (successful_caches / total_breeds) * 100
    else:
        percentage = 0
    return f"Cached data for {percentage:.2f}% of breeds."

def get_longest_breed(cache_file):
    cache = load_json(cache_file)
    longest_breed = None
    longest_life = 0

    for url, data in cache.items():
        if data.get('status_code') == 200 and data.get('data') is not None:
            breed_data = data['data']
            life_info = breed_data['attributes'].get('life', {})
            max_life = life_info.get('max')
            breed_name = breed_data['attributes']['name']

            if max_life is not None:
                if max_life > longest_life:
                    longest_life = max_life
                    longest_breed = (breed_name, max_life)
                elif max_life == longest_life and longest_breed is not None:
                    if breed_name < longest_breed[0]:
                        longest_breed = (breed_name, max_life)
            
    if longest_breed:
        return longest_breed
    else:
        return "No breeds found"
    
def get_groups_above_cutoff(cutoff, cache_file):
    cache = load_json(cache_file)
    groups = {}
    group_counts = {}

    

    for url, data in cache.items():
        if data.get('status_code') == 200 and data.get('data') is not None:
            breed_data = data['data']
            life_info = breed_data['attributes'].get('life', {})
            max_life = life_info.get('max')

            if max_life is not None and max_life >= cutoff:
                if ('relationships' in breed_data and 
                    'group' in breed_data['relationships'] and 
                    'data' in breed_data['relationships']['group'] and 
                    'id' in breed_data['relationships']['group']['data']):
                    group_id = breed_data['relationships']['group']['data']['id']
                    if group_id not in groups:
                        groups[group_id] = 0
                    group_counts[group_id] += 1

    return list(groups)

#Extra Credit
def recommend_breeds_in_same_group(breed_name, cache_file):
    cache = load_json(cache_file)
    target_group_id = None
    recommendations = []
    breed_found = False

    if not cache:
        return "No breed data found in cache."

    for url, data in cache.items():
        if data.get('status_code') == 200 and data.get('data') is not None:
            breed_data = data['data']
            if breed_data['attributes']['name'] == breed_name:
                breed_found = True
                if ('relationships' in breed_data and 
                    'group' in breed_data['relationships'] and 
                    'data' in breed_data['relationships']['group'] and 
                    'id' in breed_data['relationships']['group']['data']):
                    target_group_id = breed_data['relationships']['group']['data']['id']
                break

    if not breed_found:
        return f"'{breed_name}' is not in the cache."
    if target_group_id is None:
        return f" No group information available for '{breed_name}'."

    for url, data in cache.items():
        if data.get('status_code') == 200 and data.get('data') is not None:
            breed_data = data['data']
            if ('relationships' in breed_data and 
                'group' in breed_data['relationships'] and 
                'data' in breed_data['relationships']['group'] and 
                'id' in breed_data['relationships']['group']['data'] and 
                breed_data['relationships']['group']['data']['id'] == target_group_id):
                recommendations.append(breed_data['attributes']['name'])

    recommendations.remove(breed_name)
    if not recommendations:
        return f"No recommendations found based on '{breed_name}'."
    
    return recommendations
