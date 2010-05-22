# -*- coding: utf-8 -*-
#
# Copyright 2010
# Ionuț C. Arțăriși <mapleoin@fedoraproject.org>
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os.path
import re
import urllib

import yum.packages
import rpmUtils.transaction

import func_module

FEDORA_LICENSES = 'https://fedoraproject.org/w/index.php?title=Licensing:Main&action=raw&section=%s'
CODE_SECTION = 8
# Section numbers SHOULD be viewable here? But the index api apparently only
# uses integer numbers
# https://fedoraproject.org/w/api.php?text={{Licensing:Main}}&action=parse&prop=sections
# LICENSE_SECTIONS = [8, 13, 16,
# fails for any value >19 and so skips Fonts section

# All this part should go away if we can get a more structured Licenses list
def lpages(licenses_url, section):
    '''Retrieves the license page
    '''
    f = urllib.urlopen(licenses_url % section)
    license_page = f.read()
    f.close()
    return license_page

def get_licenses_from_page(license_page):
    # We have to rely on the structure of the current wiki page and hope it
    # never changes
    regy = re.compile(r"""\|-\n\|    # beginning of a good row
                       .*?\|\|       # skip the first column
                       \s*(.*?)\s*   # get our column and strip whitespace
                       \|\|          # end our column
                       """, re.X)
    licenses = set()

    # First one is the table header
    [licenses.add(l) for l in re.findall(regy, license_page)[1:]]
    return licenses

class Flice(func_module.FuncModule):

    # Update these if need be.
    version = "0.0.1"
    api_version = "0.0.1"
    description = "check if an srpm's license is approved by Fedora"

    lpage = lpages(FEDORA_LICENSES, CODE_SECTION)
    good_licenses = get_licenses_from_page(lpage)

    def check(self, srpm_path):
        """Check the SRPM on the given path for Fedora License compliance

        Receives a 'file://' or 'http(s)://' path to a SRPM, downloads the
        file if necessary, extracts the yum metadata and compares to our
        list of licenses.
        """
        if 'file://' in srpm_path:
            pkg_path = srpm_path.replace('file://','')
            if not os.path.isfile(pkg_path):
                return "Couldn't find the srpm file: %s." % pkg_path
        elif 'http' in srpm_path:
            try:
                pkg_path = urllib.urlretrieve(srpm_path)[0]
            except:
                return "Couldn't open the url: %s" % pkg_path
        else:
            return "Don't know how to open that."

        ts = rpmUtils.transaction.initReadOnlyTransaction()
        package = yum.packages.YumLocalPackage(ts, pkg_path)

        pkglicense = set(re.split("\s+and\s+", package.license))
        if pkglicense.issubset(self.good_licenses):
            return (package.license, 'Good.')
        else:
            return (package.license, 'Probably Bad.')

    def register_method_args(self):
        return {
            'check': {
                'args' : {
                    'srpm_path':{
                        'type':'string',
                        'optional':False,
                        'default':'',
                        'description':'file:// path or http:// to the srpm'
                        },
                    },
                'description': 'Check the license of a srpm for '
                               'Fedora compliance'
                }
            }
