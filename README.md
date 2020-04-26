My goal is to make this fork the go to library for the etsy api. Please use and file bugs

changelog (since fork)
- made compatible with python 3.4+
- fixed bug where oauth client didnt work because etsy rejects calls with the api_key param for clients using oauth
- removed EtsySandboxEnv because etsy doesnt seem to have a sandbox env anymore.
- replaced simplejson with builtin json, replaced python-oauth2 with requests-oauthlib.
- removed methods on etsy oauth client for creating the oauth token. for now the credentials must be retrieved with a
a separate workflow and passed into the etsy oauth client. This simplifies the ctor because before it wasn't obvious
which parameters needed to be passed to the client for each use case.
- added basic support for PUT and delete methods.
- added helpers to make getting oauth credentials from etsy easier.

TODO
- make reading the key from a file work with python3
- package for pip instead of easy_install
- fix package imports - seems like there is probably a way to get relative naming working
- document the method table cache is only worth while for development. it only saves 1 call on each startup.
- document how to use the oauth client vs the normal api client
- fix all tests (dont test anything that costs money like listing)
- add at least 1 method per test per client (oauth client and unauth'd/api key client)
- for the gets need to test a get that doenst require auth (no permission scope) and one that does
- test PUT/DELETE - unsure if original library handled them

# etsy-python
Python access to the Etsy API

Originally By Dan McKinley - dan@etsy.com - [http://mcfunley.com](http://mcfunley.com)
Forked by Sean Scheetz

## Installation

The simplest way to install the module is using 
[setuptools](http://pypi.python.org/pypi/setuptools).

<pre>
$ easy_install etsy
</pre>

To install from source, extract the tarball and use the following commands.

<pre>
$ python setup.py build
$ sudo python setup.py install
</pre>

## Simple Example

To use, first [register for an Etsy developer key](http://developer.etsy.com/).
Below is an example session. 

<pre>
$ python
python
Python 2.5.1 (r251:54863, Feb  6 2009, 19:02:12) 
[GCC 4.0.1 (Apple Inc. build 5465)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from etsy import Etsy
>>> api = Etsy('YOUR-API-KEY-HERE')
>>> api.getFrontFeaturedListings(offset=10, limit=1)[0]['title']
'Artists Eco Journal -  Landscape Watercolor - Rustic Vegan Hemp and Recycled Rubber'
</pre>


See also [this blog post](http://codeascraft.etsy.com/2010/04/22/announcing-etsys-new-api/)
on Code as Craft.


## Configuration

For convenience (and to avoid storing API keys in revision control
systems), the package supports local configuration. You can manage
your API keys in a file called $HOME/etsy/keys (or the equivalent on
Windows) with the following format:

<pre>
v2 = 'Etsy API version 2 key goes here'
</pre>

Alternatively, you can specify a different key file when creating an API object.

<pre>
from etsy import Etsy

api = Etsy(key_file='/usr/share/etsy/keys')
</pre>

(Implementation note: the keys file can be any valid python script that defines
a module-level variable for the API version you are trying to use.)

## Tests

This package comes with a reasonably complete unit test suite. In order to run
the tests, use:

<pre>
$ python setup.py test
</pre>

Some of the tests (those that actually call the Etsy API) require your API key
to be locally configured. See the Configuration section, above.


## Method Table Caching

This module is implemented by metaprogramming against the method table published
by the Etsy API. In other words, API methods are not explicitly declared by the
code in this module. Instead, the list of allowable methods is downloaded and 
the patched into the API objects at runtime.

This has advantages and disadvantages. It allows the module to automatically 
receive new features, but on the other hand, this process is not as fast as 
explicitly declared methods. 

In order to speed things up, the method table json is cached locally by default.
If a $HOME/etsy directory exists, the cache file is created there. Otherwise, it 
is placed in the machine's temp directory. By default, this cache lasts 24 hours.

The cache file can be specified when creating an API object:

<pre>
from etsy import Etsy

api = Etsy(method_cache='myfile.json')
</pre>

Method table caching can also be disabled by passing None as the cache parameter:

<pre>
from etsy import Etsy

# do not cache methods
api = Etsy(method_cache=None)
</pre>


## Version History


### Version 0.3.1
* Allowing Python Longs to be passed for parameters declared as "integers" by the API 
  (thanks to [Marc Abramowitz](http://marc-abramowitz.com)). 


### Version 0.3 
* Support for Etsy API v2 thanks to [Marc Abramowitz](http://marc-abramowitz.com). 
* Removed support for now-dead Etsy API v1. 


### Version 0.2.1 
* Added a cache for the method table json.
* Added a logging facility.


### Version 0.2 - 05-31-2010
* Added local configuration (~/.etsy) to eliminate cutting & pasting of api keys.
* Added client-side type checking for parameters.
* Added support for positional arguments.
* Added a test suite.
* Began differentiation between API versions.
* Added module to PyPI. 

### Version 0.1 - 05-24-2010 
Initial release