# Copy to config.py (gitignored) and fill in. Nothing here is committed with real values.

# Local paths.
pc_username = ""
download_path = "/path/to/downloads"
beacon_park_info_path = "/path/to/beacon_park_info.csv"

# The property-management system the readings are imported into.
kmc_url = "https://portal.example.com"
kmc_username = ""
kmc_password = ""

# Vendor portals.
abt_url_start = "http://abt.example.com/Usage%20Reports/All/"
cereniti_url = "https://cereniti.example.com"
cereniti_username = ""
cereniti_password = ""
beacon_url = "https://beacon.example.com/admin/portfolio/at_a_glance"
beacon_username = ""
beacon_password = ""

# Properties: title -> details. abt_url is the property's report page under abt_url_start (ABT jobs only).
property_info = {
    "Example Property": {"title": "Example Property", "shortname": "example", "propid": 1, "day": 10,
                         "abt_url": "Example%20Property.html"},
}
# Which properties the ABT job imports.
abt_properties = ["Example Property"]
