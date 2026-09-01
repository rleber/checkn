# checkn

Check if a name is already defined somewhere

## Description

Tool to check if a name is defined name:
- For Python
  - A builtin class
  - A builtin module
  - A module in the standard libraries
  - An installable library
  - An installed library on the current system
- For Ruby
  - A builtin class
  - A gem
- For Git
  - A repository created by this user
- For the shell
  - A zsh reserved word
  - A bash reserved word
  - An alias defined on this system
  - A function defined on this system
  - A program defined on this system

## Implementation
Checkn runs analyses in separate areas of concern (e.g. Ruby, Shell), which
it calls domains. In each domain, there are analyses (e.g. to answer the 
question: is this name a Shell reserved word?). Analyses are performed on the results of tests (e.g. running the `type` command in a shell). Tests are dispatched by name through the use of a helper called a "lab".

Domains, labs, analyses, and tests are dynamically defined by importing Python
scripts within a directory structure:

src/checkn/: 
├── cli.py: the main script that invokes domains to analyze names
├── domains/: Contains the definition of domains, e.g.
|   ├── shell/: Contains the definition of the shell domain, analyses and tests
|   │   ├── domain.py: Defines the domain class for the shell domain
|   │   ├── lab.py: Defines the lab class for the shell domain
|   │   ├── analyses/: Contains the definitions of analyses in the domain, e.g.
|   |   │   ├── alias_analysis.py: Code to analyze: is this name a shell alias?
|   |   │   └ ...
|   │   └── tests/: Contains the definitions of tests in the domain, e.g.
|   |       ├── bash_type_test.py: Code to run a `type` test in the bash shell
|   |       └ ...
|   └ ...
├── core/: Defines core code, like abstract class definitions, e.g.
│   ├── name_domain.py: The abstract base class for domain classes
│   └ ...
└── utils/: Contains shared classes and functions, e.g.
    ├── discovery.py: Defines the discover_classes function, which is used
    |                 by several classes to find dynamic class definitions
    └ ...

## Getting Started

### Dependencies

requests

### Installing

`pip install checkn`

### Executing program

`checkn <name>`

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


