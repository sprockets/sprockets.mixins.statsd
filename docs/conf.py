from sprockets.mixins.statsd import __version__

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.httpdomain',
]
templates_path = []
source_suffix = '.rst'
master_doc = 'index'
project = 'sprockets.mixins.statsd'
copyright = '2014-2021, AWeber Communications'
release = __version__
version = '.'.join(release.split('.')[0:1])
exclude_patterns = []
intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'requests': ('https://requests.readthedocs.org/en/latest/', None),
    'sprockets': ('https://sprockets.readthedocs.org/en/latest/', None),
}
