Redesign to speed up checkn by caching

Many tests in checkn are slow. See benchmarks in data/time_tests.py
I believe its execution could be sped up considerably by caching, since the results from most tests (e.g. is it a shell alias, as determined by the test `type -aw`?) don't change very often.
When test results do change, it's most likely that they go from a "no" to a "yes" -- for instance, a new alias definition gets added to .zshrc
The cache should be persistent, and stored in a simple form. I suggest a sqlite3 database, storing the results of tests.
There should be one system-wide cache. It should reside in my user root directory, named .checkn_cache.db
The cache should note the datetime (UTF) at which the cached results in each domain were last updated.
If checkn is invoked to check a name and needed sections of the cache are empty, it should reload them.
I would like to keep cache management neatly separated from running name checks. The current user interface for checkn should not change. You may create a separate executable entrypoint for checkn or a subcommand for cache management. For now, relevant cache management functions include:
- Building or rebuilding the cache database
- Showing the path of the cache database
- Forcing all or selected domain caches to be cleared
- Reloading all or selected domain caches
- Listing the status of domain caches: how many entries in them, when were they last updated?
Some tests and analyses will need to be changed for the cache to save much time. Tests will not be sped up much if they check the status of individual names (unless the user is repeated checking the status of the same name, which is unlikely); they should test multiple names -- all if possible. Then the related analyses will need to be modified to work with the new test. For example the test related to determining if a name is a zsh alias (type_aw_interactive_test.py) currently checks a single name. To be sped up significantly, it would have to check many or all aliases (perhaps using the `alias` command), and the analysis should check against that.
To maximize impact, we should begin by optimizing the the tests that are slowest. Indeed, some tests are so fast that the effort necessary to cache their results is probably not worth the effort, and perhaps even counter-productive. (Therefore, it should not be assumed that caching is used for all tests.)
The slowest of the current tests is testing if a name is a pypi module, based on querying pypi.org. Let's begin by creating a caching mechanism for only that test.
I agree with your recommendation for approaching caching results from pypi using a nightly resync, thus avoiding the complexity of incremental updates.