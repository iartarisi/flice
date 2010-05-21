Flice is a func module that checks SRPMS for Fedora License conformance

The module checks if the license(s) specified by the packager in the .spec
file belong to the list of accepted Fedora Licenses:
http://fedoraproject.org/wiki/Licensing

Right now it just downloads one of the wiki sections and parses the HTML to
get a license list.



