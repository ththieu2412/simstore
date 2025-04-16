# Hằng số
DATE_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",   # 2025-03-04 08:30:00
    "%Y-%m-%dT%H:%M:%SZ",  # 2025-03-04T08:30:00Z (ISO 8601)
    "%Y-%m-%dT%H:%M:%S%z", # 2025-03-04T08:30:00+07:00
]
DATE_OUTPUT_FORMAT = "%H:%M:%S %d-%m-%Y"  # 08:30:00 04-03-2025