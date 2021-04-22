"""This file contains bank's config"""

BANKS_CONFIG: dict = {
    "bank1": {
        "transform_to": [],
        "replace_keys": {
            "timestamp": "date",
        },
        "date_format": "%b %d %Y",
    },
    "bank2": {
        "transform_to": [],
        "replace_keys": {"transaction": "type", "amounts": "amount"},
        "date_format": "%d-%m-%Y",
    },
    "bank3": {
        "transform_to": [["divide", "cents", 100], ["add_fields", "euro", "cents"]],
        "replace_keys": {"date_readable": "date", "euro": "amount"},
        "date_format": "%d %b %Y",
    },
}

UNIFIED_BANK_HEADER: list = ["date", "type", "amount", "from", "to"]
