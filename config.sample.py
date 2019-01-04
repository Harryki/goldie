# -*- coding: utf-8 -*-
"""
File: config.sample.py
- Copy `config.sample.py` to `config.py`.
"""

# Subscription Key for calling the Cognitive Face API.
FACE_API_KEY = "your_face_api_key"

# subscription key for speach API
SPEACH_API_KEY = "your_speach_api_key"

# Base URL for calling the Cognitive Face API.
BASE_URL = "your_base_url"

# Time (in seconds) for sleep between each call to avoid exceeding quota.
# Default to 3 as free subscription have limit of 20 calls per minute.
TIME_SLEEP = 3

# group id can be set by user but has to be a string, e.g. "foo_bar" or "hello_world"
GROUP_ID = "your_group_id"