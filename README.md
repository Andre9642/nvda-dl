# NVDA-dl
Small Python script to download latest NVDA versions (alpha, beta and stable).

```
Usage: nvda-dl [options]

Options:
  -h, --help            show this help message and exit
  -d DOWNLOAD_DIR, --download-dir=DOWNLOAD_DIR
                        download dir
  -t VERSIONTYPES, --version-type=VERSIONTYPES
                        version type (stable, beta, alpha)

Examples:
$ nvda-dl -t stable -d out
$ nvda-dl -t alpha -t beta
$ nvda-dl -t alpha -t beta -t stable
```