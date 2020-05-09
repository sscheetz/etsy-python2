## Intro
Updated version of [etsy-python](https://github.com/mcfunley/etsy-python) with python3
compatability and support for the modern etsy api. Please file any bugs, suggestions,
or usage questions as github issues and I will get to them as soon as possible.

Note, the tests are not yet upgraded (they should be within a few days) and I have not tested all features (notably I doubt specifying a keyfile works currently), but I wanted to get this package out there in case anyone was looking for a functional package in 2020 (and because I need it). I am currently successfully using it in my personal projects.

See changelog at bottom of the readme for differences between etsy-python and etsy-python2. The
last release for etsy-python was 0.3.1.

## etsy-python2
Python access to the Etsy API

Originally By Dan McKinley - dan@etsy.com - [http://mcfunley.com](http://mcfunley.com)

Forked by Sean Scheetz

## Installation

The simplest way to install the module is pip

<pre>
$ pip install etsy2
</pre>

To install from source, extract the tarball and use the following commands.

<pre>
$ python setup.py build
$ sudo python setup.py install
</pre>

## Overview

This library works by retrieving the api metadata from https://api.etsy.com/v2/?api_key=<your-api-key> and patching the methods onto the `Etsy` object at runtime. This happens during
construction of the `Etsy` object (the api client). Refer to the [Etsy API docs](https://www.etsy.com/developers/documentation/reference/apimethod) to see what method names you can call from the `Etsy` object. Every parameter can be passed in as a named parameter to the method call. e.g.

```python
etsy.findAllShopReceipts(shop_id=<shop_id>)
```

## Usage

There are two types of etsy endpoints: Those that require OAuth and those that don't. For endpoints that don't require OAuth you can use the regular etsy client provided by this library as shown below.

```python
from etsy2 import Etsy

etsy = Etsy(api_key=<your-api-key>)
etsy.findAllFeaturedListings()
```

For endpoints that do require OAuth you must pass an `EtsyOAuthClient` to the `Etsy` constructor.

```python
etsy_oauth = EtsyOAuthClient(client_key=api_key,
                            client_secret=shared_secret,
                            resource_owner_key=oauth_token,
                            resource_owner_secret=oauth_token_secret)
etsy = Etsy(api_key=api_key, etsy_oauth_client=etsy_oauth)
```

The `EtsyOAuthClient` requires a client_key, client_secret, resource_owner_key, and resource_owner_secret to be constructed. The client_key and the client_secret are the keystring and shared secret given to you by etsy upon registering your app. The resource_owner_key and resource_owner_secret are the oauth_token and oauth_token_secret that must be retrieved by working through etsy's oauth workflow. The `EtsyOAuthHelper` exists so simplify the creation of the two aforementioned credentials. An example of how to use the `EtsyOAuthHelper` is given below.

```python
# define permissions scopes as defined in the 'OAuth Authentication' section of the docs
# https://www.etsy.com/developers/documentation/getting_started/oauth#section_permission_scopes
permission_scopes = ['transactions_r', 'listings_r']

# login_url is the url to redirect the user to to have them authenticate with etsy.
# temp_oauth_token_secret is the secret used in the get_ouath_token method to retrieve permanent oauth credentials.
# <callback_url> is the url you want etsy to redirect the user to after logging in to etsy.
login_url, temp_oauth_token_secret = EtsyOAuthHelper.get_request_url_and_token_secret(api_key, shared_secret, permission_scopes, <callback_url>)

# called in the handler for <callback_url> to retrieve oauth crendentials for the user whose data you are interacting with
oauth_token, oauth_token_secret = EtsyOAuthHelper.get_oauth_token(api_key, shared_secret, temp_oauth_token_secret, input('paste: '))
```

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

As mentioned above, this module is implemented by metaprogramming against the method table
published by the Etsy API. In other words, API methods are not explicitly declared by the
code in this module. Instead, the list of allowable methods is downloaded and
the patched into the API objects at runtime.

This has advantages and disadvantages. It allows the module to automatically
receive new features, but on the other hand, this process is not as fast as
explicitly declared methods.

In order to speed things up, the method table json is cached locally by default.
If a $HOME/etsy directory exists, the cache file is created there. Otherwise, it
is placed in the machine's temp directory. By default, this cache lasts 24 hours.

The cache file can be specified when creating an API object:

```python
from etsy import Etsy

api = Etsy(method_cache='myfile.json')
```

Method table caching can also be disabled by passing None as the cache parameter:

```python
from etsy import Etsy

# do not cache methods
api = Etsy(method_cache=None)
```


## Version History

### Version 0.4.0
- Added python 3 compatability
- Removed EtsySandboxEnv because etsy doesnt seem to have a sandbox env anymore.
- Fixed broken EtsyOauthClient because etsy now rejects calls including the api_key param when oauth is being used.
- Replaced simplejson with builtin json, replaced python-oauth2 with requests-oauthlib (python-oauth2 only supports up to python 3.4).
- Removed the oauth credential retrieval methods from EtsyOAuthClient to make client usage easier.
- Created EtsyOAuthHelper to make retrieving the etsy oauth credentials easier.
- Added helpers to make getting oauth credentials from etsy easier.
- Added basic support for PUT and DELETE methods (which the etsy api didnt have when this was originally written)

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