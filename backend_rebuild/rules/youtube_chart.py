FOLLOWER_RANGE_RULES = {
    "free": ["28d"],
    "premium": ["28d", "90d", "180d", "365d"]
}

HASHTAG_RANGE_RULES = {
    "free": {
        "ranges": ["5"],
        "hashtag_limit": 3
    },
    "premium": {
        "ranges": ["5", "8", "12"],
        "hashtag_limit": 10
    }
}

RANGE_DAYS = {
    "28d": 28,
    "90d": 90,
    "180d": 180,
    "365d": 365
}
