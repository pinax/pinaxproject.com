import posixpath
import re
import urllib2
import urlparse

from downloads.verlib import NormalizedVersion


_href_re = re.compile('href=(?:"([^"]*)"|\'([^\']*)\'|([^>\\s\\n]*))', re.I|re.S)
_clean_re = re.compile(r'[^a-z0-9$&+,/:;=?@.#%_\\|-]', re.I)
_egg_info_re = re.compile(r'([a-z0-9_.]+)-([a-z0-9_.-]+)', re.I)


class Link(object):
    
    @classmethod
    def dirty(cls, url):
        url = _clean_re.sub(lambda m: "%%%2x" % ord(m.group(0)), url)
        return cls(url)
    
    def __init__(self, url):
        self.url = url
    
    @property
    def path(self):
        return urlparse.urlsplit(self.url)[2]
    
    def splitext(self):
        path = posixpath.basename(self.path.rstrip("/"))
        base, ext = posixpath.splitext(path)
        if base.lower().endswith(".tar"):
            ext = base[-4:] + ext
            base = base[:-4]
        return base, ext
    
    _egg_fragment_re = re.compile(r'#egg=([^&]*)')
    
    @property
    def egg_fragment(self):
        m = self._egg_fragment_re.search(self.url)
        if not m:
            return None
        return m.group(1)


def parse_versions(distribution, content):
    """
    Given a bunch of HTML (content) work out what versions are on the page.
    """
    search_name = distribution
    links = []
    for match in _href_re.finditer(content):
        url = match.group(1) or match.group(2) or match.group(3)
        links.append(Link.dirty(url))
    for link in links:
        if link.egg_fragment:
            egg_info = link.egg_fragment
        else:
            egg_info, ext = link.splitext()
            if not ext:
                continue
            if egg_info.endswith(".tar"):
                # Special double-extension case:
                egg_info = egg_info[:-4]
                ext = ".tar" + ext
            if ext not in [".tar.gz", ".tar.bz2", ".tar", ".tgz", ".zip"]:
                continue
        m = _egg_info_re.search(egg_info)
        if not match:
            version = None
        name = m.group(0).lower()
        # to match the "safe" name that pkg_resources creates
        name = name.replace("_", "-")
        if name.startswith(search_name.lower()):
            version = m.group(0)[len(search_name):].lstrip("-")
        else:
            version = None
        if version is None:
            continue
        yield NormalizedVersion(version)


def latest_version(distribution, index_url):
    url = posixpath.join(index_url, distribution)
    content = urllib2.urlopen(url, timeout=1).read()
    versions = parse_versions(distribution, content)
    return sorted(versions, reverse=True)[0]
