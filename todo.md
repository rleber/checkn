Future direction:

Define several classes

- NameTest object
  - Has a title
  - Performs an test (e.g. `type -aw <name>`) on a name
  - Returns a string
  - The results for any name are cached
- NameLab object
  - Has a title
  - Has a path, which points to a directory
  - Is a singleton (there is only one Lab with a given title)
  - Automatically registers NameTest objects, each of which is defined
    in a file in the directory, by loading all the matching files
    "xxx_test.py" in the directory
  - Has a list() method which returns a list[str] of all the titles of all
    the NameTests it knows
  - Has an execute(title: str, name: str) method, which performs the
    NameTest with the matching title on the name
  - Has an execute_all(name: str) method, which performs all the analyses it
    knows on the name, returning a dict[str, str] = {title: analysis_result, ...}
- NameAnalysis object
  - Has a title
  - Is given an NameLab
  - Performs an analysis on a name (e.g. is it a builtin keyword in zsh?), making use of the results of one or more tests (i.e. NameTests)
  - Asks the NameLab to run the needed NameTests (by their ttiles), and
    analyzes the results
  - Returns a string containing the results
  - The results for any name are cached
- NameDomain object (currently called Contexts)
  - Has a title
  - Has a path, which points to a directory
  - Has an NameLab
  - Is a singleton (there is only one NameDomain with a given title)
  - Automatically registers NameAnalysis objects, each of which is defined
    in a file in the directory, by loading all the matching files
    "xxx_analysis.py" in the directory
  - Has a list() method which returns a list[str] of all the titles of all
    the NameAnalyses it knows
  - Has an execute(title: str, name: str) method, which performs the
    NameAnalysis with the matching title on the name
  - Has an execute_all(name: str) method, which performs all the analyses it
    knows on the name, returning a dict[str, str] = {title: analysis_result, ...}
- NameManager class
  - Abstract base class for NameLab and NameDomain
  - Defines the registry and dispatch functionality neede by NameLab and NameDomain, i.e. finding methods in a directory, listing them, executing them

Rewrite the contexts: ShellContext, PythonContext, GitContext, and RubyContext (which are defined in src/checkn/contexts) as instances of class NameDomain, with associated NameLabs, NameTests, and NameAnalyses as needed, and with source files in a directory structure like the following:

Directory structure (within ~/projects/python/checkn):
- src/checkn/ 
  - Contains the main script (cli.py) that invokes NameDomains to test names
  - Contains other necessary elements of the pip module (e.g. __init__.py)
- src/checkn/utils: Contains any shared utility classes or functions
- src/checkn/domains: Contains the definitions of the NameDomains, each NameDomain residing in a subdirectory along with the associated NameLabs, NameTests, and NameAnalyses, e.g. 
  - the NameDomain for shell analyses would be in src/checkn/domains/shell/domain.py, i
  - Its associated NameLab would be in src/checkn/domains/shell/lab.py
  - The analyses associated with the NameDomain would be in src/checkn/domains/shell/analyses/
  - The tests associated with the NameLab would be in src/checkn/domains/shell/tests/

Note that shell_context has already been refactored to put its analyses (called checks) in a directory src/checkn/contexts/shell/checks/. The other Contexts are of a previous iteration of the code structure; their analyses are integrated into the code of the Context