# Data Collectors

Data collection is handled entirely by [posture](https://github.com/massyn/posture)
([PyPI](https://pypi.org/project/posture/)) — a Python library that pulls data from
security tools and returns it as DataFrames. This repo contains no collector code of
its own; it uses posture's `posturecollect` command-line tool to write every table to
Parquet files in the `data` folder.

## Quick Start

```bash
pip install -r requirements.txt                                   # installs posture
posturecollect --output data/source                               # run from the repo root
posturecollect --include cve_db.cve_summary --output data/source  # needed by the vm_* metrics
```

`run.sh` in the repo root runs the collection (including the no-auth `cve_db`,
`macadmins` and `endoflife` sources) and then starts the dashboard.

With no other flags, `posturecollect` collects from every source that has all of
its required environment variables set, and writes one Parquet file per table:

```
data/source/<source>_<resource>.parquet     e.g. data/source/crowdstrike_hosts.parquet
```

Each run overwrites these files, so `data/source` always holds the latest snapshot.

## Configuration

posture reads credentials from environment variables, and loads a `.env` file from
the current directory (or a parent) on its own. Variables already set in the shell
override values in `.env`. Each source's required variables are listed in
[posture's collector docs](https://github.com/massyn/posture/blob/main/docs/index.md), for example:

```bash
# .env
CROWDSTRIKE_CLIENT_ID=xxx
CROWDSTRIKE_CLIENT_SECRET=xxx

POSTURE_OUTPUT=data/source               # used when --output isn't given
```

## Common Options

```bash
posturecollect --include crowdstrike endoflife   # only these sources (also the only way to run no-auth sources)
posturecollect --include crowdstrike.hosts       # just one table (<source>.<resource>)
posturecollect --exclude qualys snyk.issues      # everything configured, minus these
posturecollect --history                         # one dated file per table per day instead of overwriting
posturecollect --thread 5                        # collect this many sources at the same time (default 3)
posturecollect --env .env.nonprod                # use a different env file
posturecollect --debug                           # verbose logging
```

`--include`, `--exclude`, `--output`, `--history` and `--thread` can also be set as
`POSTURE_INCLUDE`, `POSTURE_EXCLUDE`, `POSTURE_OUTPUT`, `POSTURE_HISTORY` and
`POSTURE_THREAD`. If both are set, the flag wins.

With `--history`, files are written as
`data/source/<source>_<resource>/<YYYY.MM.DD>.parquet`.

A failure in one source or table is logged and doesn't stop the rest of the run.
`posturecollect` exits non-zero if anything failed and prints a summary table at the end.

## Supported Sources

See [posture's docs](https://github.com/massyn/posture/blob/main/docs/index.md) for
every supported source, its environment variables, and the column schema of every table.
You can also list them in Python:

```python
from posture import catalog, runnable_sources

catalog()            # every source, resource and column
runnable_sources()   # only the sources whose credentials are set right now
```
