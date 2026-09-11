# checkn

Check if a name is already defined somewhere

## Description

Tool to check if a name is defined name:
- For Python
  - A builtin class
  - A builtin module
  - A module in the standard libraries
  - A module's import name (when different from its installed package name)
  - An installed library on the current system
  - A package published on PyPI but not installed locally
- For Ruby
  - A builtin class
  - An installed gem
  - A gem published on rubygems.org but not installed locally
- For Homebrew
  - An installed formula
  - A formula published in homebrew-core but not installed locally
  - An installed cask
  - A cask published in homebrew-cask but not installed locally
- For apt
  - An installed package (Linux only)
  - A package known to Debian's package archive but not installed locally
    (works on any OS)
- For JavaScript
  - A reserved keyword
  - A builtin class (e.g. Array, Map, Promise)
  - A Node.js builtin module
  - An npm package installed globally on this system
  - A package published on npm but not installed locally
- For Git
  - A repository created by this user
- For the shell
  - A zsh reserved word
  - A bash reserved word
  - An alias defined on this system
  - A function defined on this system
  - A program defined on this system

The "published" Homebrew checks (formula/cask, but not installed-formula/
installed-cask) read Homebrew's own local cache of known names rather than
querying the network. That cache is an undocumented Homebrew implementation
detail, not a stable public API -- see `domains/homebrew/api_cache.py` for
the specifics and how a missing or malformed cache is handled.

The apt "installed package" check shells out to `dpkg-query` and only
runs on Linux, where dpkg actually exists -- see `utils/os_support.py`
for how a probe declares itself platform-restricted. The apt "package"
check, by contrast, needs no local apt/dpkg at all: it fetches Debian's
own published package index (`packages.debian.org/stable/allpackages`)
over the network, so it works and can classify names on any OS.

The "package published on npm but not installed locally" check has no
bulk index to cache the way its Python/Ruby/Homebrew counterparts do (npm's
full package list runs to hundreds of megabytes), so it queries the npm
registry live, once per check, instead -- see
`domains/javascript/probes/npm_module_probe.py`.

## Implementation
Checkn runs analyses in separate areas of concern (e.g. Ruby, Shell), which
it calls domains. In each domain, there are analyses (e.g. to answer the 
question: is this name a Shell reserved word?). Analyses are performed on the results of probes (e.g. running the `type` command in a shell). Probes are dispatched by name through the use of a helper called a "lab".

Domains, labs, analyses, and probes are dynamically defined by importing Python
scripts within a directory structure:

src/checkn/: 
├── cli.py: the main script that invokes domains to analyze names
├── domains/: Contains the definition of domains, e.g.
|   ├── shell/: Contains the definition of the shell domain, analyses and probes
|   │   ├── domain.py: Defines the domain class for the shell domain
|   │   ├── lab.py: Defines the lab class for the shell domain
|   │   ├── analyses/: Contains the definitions of analyses in the domain, e.g.
|   |   │   ├── alias_analysis.py: Code to analyze: is this name a shell alias?
|   |   │   └ ...
|   │   └── probes/: Contains the definitions of probes in the domain, e.g.
|   |       ├── type_aw_probe.py: Code to run a `type -aw` probe in zsh
|   |       └ ...
|   └ ...
├── core/: Defines core code, like abstract class definitions, e.g.
│   ├── name_domain.py: The abstract base class for domain classes
│   ├── cacheable_probe.py: Base class for probes backed by the persistent cache
│   └ ...
├── cache.py: CacheDB, the sqlite3-backed persistent cache
├── cache_cli.py: the checkn-cache script for cache management
└── utils/: Contains shared classes and functions, e.g.
    ├── discovery.py: Defines the discover_classes function, which is used
    |                 by several classes to find dynamic class definitions
    └ ...

## Caching

Some probes are expensive (e.g. `pypi module`, which otherwise has to fetch
and parse PyPI's entire package index on every check). Probes that fetch a
bulk, rarely-changing result set can subclass `CacheableNameProbe`
(`core/cacheable_probe.py`) instead of `NameProbe`, implementing `_fetch_all`
in place of `_perform`. The base class handles storing/looking up results
in a single, system-wide sqlite3 cache at `~/.checkn_cache.db` (`cache.py`),
and transparently reloads a probe's section the first time it's needed.

Cache management is kept separate from `checkn` itself via a second
entrypoint, `checkn-cache`:

```
checkn-cache build            # ensure the cache exists and reload every cacheable probe
checkn-cache reload [-d ...]  # reload cacheable probes, all domains or the ones given
checkn-cache clear [-d ...]   # delete cached rows, all domains or the ones given
checkn-cache status [-d ...]  # entry counts and last-updated time per cached section
checkn-cache path             # print the resolved cache database path
```

`checkn` itself only reloads a section automatically if it's never been
loaded; keeping the cache fresh afterward (e.g. via a periodic `checkn-cache
reload`) is up to the user.

## Getting Started

### Dependencies

requests

### Installing

`pip install checkn`

### Executing program

`checkn <name>`

`checkn-cache --help` (cache management; see Caching above)

## Author

Richard LeBer  
richard.leber@gmail.com

## Version History

* 0.0.1
    * Initial release: Python only
* 1.0.0
    * Latest release: Python, Ruby, Git, Shell

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

For options, see [license.md](https://license.md/licenses/)


