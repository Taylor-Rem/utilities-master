# utilities-master

A desktop app I wrote at Kingsley Management, a property-management company, to import monthly utility
readings. Each month the readings for several properties had to be downloaded from three vendors' portals,
reshaped, and imported into the property-management system by hand. This tool runs each of those imports
as a job.

Built February – November 2025 in Python. Its first version was `utilities-tool`
(December 2024). Not maintained.

## What it does

For each vendor job (ABT, Cereniti, Beacon):

1. signs in to the vendor's portal with Selenium and downloads that month's readings per property;
2. reshapes the file with pandas into the columns the import expects;
3. opens the property-management system and runs the utility import for each property, with the right
   date and reading type.

## How it is built

- `front_end/` — PyQt5 windows to choose and run jobs; jobs run on a thread controller (`tools/`) so the
  window stays responsive.
- `job_manager/` — one module per vendor (`jobs/abt.py`, `cereniti.py`, `beacon.py`) on a shared base,
  plus the per-job settings.
- `file_manager/csv_manager.py` — reading and reshaping the downloads.
- `resmap_ops/resmap_import.py` — the import into the property-management system.

## Running it

Python 3 with PyQt5, Selenium and pandas. Copy `config.example.py` to `config.py` and fill in the
addresses, logins, paths and properties; `config.py` is gitignored. Then `python main.py`. It only works
against those vendors' portals and that company's system.
