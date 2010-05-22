FLice is a func module that checks SRPMS for Fedora License conformance

The module checks if the license(s) specified by the packager in the .spec
file belong to the list of accepted Fedora Licenses:
http://fedoraproject.org/wiki/Licensing

Right now it just downloads one of the wiki sections and parses the HTML to
get a license list.

Installation:

Just drop the flice.py file in your
/usr/lib/python-2.x/site-packages/func/minion/modules directory
and restart funcd.

Usage:

$ func minion1 call flice check 'http://archive.fedoraproject.org/pub/archive/fedora/linux/core/1/SRPMS/fedora-release-1-3.src.rpm'
{'minion1': ['GPL', 'Probably Bad.']}

'GPL' isn't a valid license name anymore (flice can't find it in the Licensing
list), but 'GPLv2' is a good name:

$ func minion1 call flice check 'http://archive.fedoraproject.org/pub/archive/fedora/linux/releases/10/Everything/source/SRPMS/fedora-release-10-1.src.rpm'
{'minion1': ['GPLv2', 'Good.']}

If you had downloaded fedora-release-10-1.src.rpm on your minion you could do:

$ func minion1 call flice check 'file:///tmp/fedora-release-10-1.src.rpm'
{'minion1': ['GPLv2', 'Good.']}
