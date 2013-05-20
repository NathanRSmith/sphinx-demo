What is Sphinx?:


   * A documentation generator tool.  It was originally created for the Python documentation but has support for other languages as well such as C/C++ & Javascript.  Sphinx uses reStructuredText as its markup language.
   * Main website: http://sphinx-doc.org/

Some features:

   * Output formats: HTML (including Windows HTML Help), LaTeX (for printable PDF versions), Texinfo, manual pages, plain text
   * Extensive cross-references: semantic markup and automatic links for functions, classes, citations, glossary terms and similar pieces of information
   * Hierarchical structure: easy definition of a document tree, with automatic links to siblings, parents and children
   * Automatic indices: general index as well as a language-specific module indices
   * Code handling: automatic highlighting using the Pygments highlighter
   * Extensions: automatic testing of code snippets, inclusion of docstrings from Python modules (API docs), andmore

Getting started:

There is a tutorial on the website titled "First Steps with Sphinx".


How CyberEye uses Sphinx:

Cybereye is composed of many Django applications that are set up as individual installable Python packages.  Each (or most) of the applications have associated documentation in the "doc" directory of the package root.  All packages are collected in a "packages" directory so they are easy to find relative to each other.  In the packages directory I have a file called "packageList.py", which my fabfile uses to understand the capabilities for each package.

```
packages/
     fabfile.py
     packageList.py
     doc/
     django-Cybereye/
          cybereye/
          doc/
          setup.py
     django-Cybereye-warehouse/
          cybereye_warehouse/
          doc/
          setup.py
     ...
```

Since most of these packages are Django apps they require a few extra lines for Sphinx to be able to load them correctly:

```python
import sys, os

path = os.path.abspath(os.path.dirname(__file__))

# insert parent into python path and packages directory
sys.path.insert(0,os.pardir)
sys.path.append('/'.join(path.split('/')[:-2]))

# set up python path for vm and server to be able to build in either
import vmpaths, serverpaths

import settings
from django.core.management import setup_environ

setup_environ(settings)

from django.core.management.commands.syncdb import Command as SyncdbCommand
SyncdbCommand().execute(verbosity=0,database='default')

autodoc_member_order = 'bysource'
```

I have Fabric commands that go through each package that has documentation and builds it.  If it is being build on the server the results are moved to a central documentation location.



