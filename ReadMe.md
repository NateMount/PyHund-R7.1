# PyHund – Revision 7.1

**Version**: R7.1 (v1.0 Alpha)  
**Author**: MountNate

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Advanced Usage](#basic-usage)
4. [Arguments](#common-arguments)
5. [Config.yaml](#️-configyaml)

---

## Overview

**PyHund** is a modular, Python-based web scraper designed with simplicity and flexibility in mind. Its core function is to search for given usernames across a range of common websites and report where they're found.

Earlier versions of PyHund became cluttered with too many competing features, which slowed development and introduced frequent bugs and edge cases.

Revision 7.1 (R7.1) takes a streamlined approach: it includes only the essentials for scraping usernames—but with a twist. PyHund is now fully extensible through a plugin system, allowing users to expand its functionality to match their specific needs with ease.

---
 

## Getting Started

To run a basic search:

```bash
pyhund <username_1> <username_2> /arg1 /arg2:value
```

Example:

```bash
pyhund JohnDoe JaneDoe "John Smith"
```

By default, PyHund works straight out of the box—no setup or prior knowledge required. Just pass in one or more usernames, and it handles the rest.

---

## Advanced Usage

For users who want more control, PyHund includes powerful arguments and configuration options. These features allow you to fine-tune behavior for custom use cases.

- Learn more in the **[Arguments](#arguments)** section.  
- Dive into deeper customization with the **[Config.yaml](#configyaml)** section.

## Arguments

PyHund supports a range of optional arguments to customize and enhance your search. Arguments may be prefixed by wither a '-' or '/'. All arguments that do not begin with either of these delimeters will be considered usernames and will be searched for in the scan.

### General Format

```bash
pyhund <usernames> /<arg>:<value>
```


### Common Arguments

- `/help` — Get help information on arguments and run settings
- `/version` — Get all version information on the program
- `/stdin:<path>` — Set file input path for usernames to be read from
- `/stdout:<flag>` — Set stdout format, defaults are (`csv, json, pipe, default`)
- `/output_path:<path>` — Set path for stdout (default is `./`)
- `debug` — Set the program into debug mode, providing info on run operations
- `verbose` — Show runtime configs and processes in verbose format
- `flags:<flag1>,<flag2>` — Set filtering flags for site scan
- `manifest:<path>` — Set alternative manifest path for custom site manifest
- `plugin-config:<plugin1>=<conf1>,<conf2>+<plugin2>...` — Configure plugins

---

## Config.yaml

For persistent settings and more complex configurations, PyHund supports a `config.yaml` file in the `/usr/local/bin/PyHund/resources` directory.

PyHund will prioritize command-line arguments over config file values when both are present.


