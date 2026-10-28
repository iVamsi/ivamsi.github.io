"""Check public paths, metadata, assets, and the preserved API without dependencies."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import json
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs, self.headings = [], [], []
        self.metadata = {}
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs:
                self.refs.append(attrs[attr])
        if tag in ('h1', 'h2', 'h3'):
            self.headings.append(int(tag[1]))
        if tag == 'img':
            assert attrs.get('alt'), 'Images need descriptive alternative text'
            assert attrs.get('width') and attrs.get('height'), 'Reserve image dimensions'
        if tag == 'meta':
            self.metadata[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'script':
            assert attrs.get('type') == 'application/ld+json', 'No runtime JavaScript needed'

for filename in ('index.html', '404.html'):
    text = (ROOT / filename).read_text(encoding='utf-8')
    doc = Document(text)
    assert len(doc.ids) == len(set(doc.ids)), 'Duplicate anchors'
    assert doc.headings.count(1) == 1, 'Exactly one main heading'
    for previous, current in zip(doc.headings, doc.headings[1:]):
        assert current <= previous + 1, 'Heading levels must not skip'
    for ref in doc.refs:
        url = urlsplit(ref)
        if not url.scheme and not url.netloc:
            assert (ROOT / url.path.lstrip('/')).exists(), f'Missing local asset: {ref}'
            if url.fragment and not url.path:
                assert url.fragment in doc.ids, f'Broken anchor: {ref}'
    assert 'charset="utf-8"' in text and 'lang="en"' in text
    if filename == 'index.html':
        assert {'libraries', 'work', 'expertise', 'about', 'contact'} <= set(doc.ids)
        for field in ('description', 'viewport', 'og:title', 'og:url', 'og:image', 'twitter:card'):
            assert doc.metadata.get(field), f'Missing metadata: {field}'
        data = text.split('<script type="application/ld+json">')[1].split('</script>')[0]
        assert json.loads(data)['@type'] == 'Person'
        assert 'https://ivamsi.github.io/' in text

api = ROOT / 'WorldCountriesAPI/api/all/index.json'
assert sha256(api.read_bytes()).hexdigest() == 'c2cdbb1db3b07aa81c571706b2d92db5a6c8c8c1840ae1f675ca9f9fd4f0516c', 'Existing API changed'
json.loads(api.read_text(encoding='utf-8-sig'))
ET.parse(ROOT / 'sitemap.xml')
assert (ROOT / 'assets/social-preview.png').is_file()
assert 'Sitemap: https://ivamsi.github.io/sitemap.xml' in (ROOT / 'robots.txt').read_text()
page_bytes = sum(p.stat().st_size for p in (ROOT / 'assets').rglob('*') if p.is_file()) + (ROOT / 'index.html').stat().st_size + (ROOT / 'styles.css').stat().st_size
assert page_bytes < 1_000_000, f'Asset budget exceeded: {page_bytes}'
print(f'PASS: anchors, local assets, metadata, heading hierarchy, API checksum, sitemap; all page assets {page_bytes:,} bytes')
