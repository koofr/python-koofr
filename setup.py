from distutils.core import setup
setup(
  name = 'koofr',
  packages = ['koofr'], # this must be the same as the name above
  install_requires=['requests'],
  version = '0.1',
  description = 'Python SDK for Koofr',
  author = 'Andraz Vrhovec',
  author_email = 'andraz@koofr.net',
  url = 'https://github.com/koofr/python-koofr', # use the URL to the github repo
  download_url = 'https://github.com/koofr/python-koofr/tarball/0.1', # I'll explain this in a second
  keywords = ['api', 'koofr', 'cloud'], # arbitrary keywords
  classifiers = [],
)
