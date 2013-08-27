#!/usr/bin/env python
import hashlib
import os
import urllib2
import time

__author__ = 'faisal'

# Hide .html (will generate all under folder)
# Note that you need to handle your links properly too
hide_html_ext = False
# Shows index.html on index paths
use_index_paths = False
# Enable/Disable sitemap generation / Enable by adding your live url
sitemap = None  # 'http://www.example.com'

url = 'http://localhost:8080/dev'
template_path = 'templates'
output_path = 'gen'

os.chdir(os.path.dirname(__file__))

if not os.path.exists(output_path):
    os.makedirs(output_path)


def generate(path):
    # Skips all _
    if path.startswith('_'):
        return

    output = os.path.join(output_path, path)
    url_path = path

    if hide_html_ext and not output.endswith('index.html'):
        output = output.split(os.sep)
        file = output.pop().split('.')
        ext = file.pop()
        output.append('.'.join(file))
        output.append('index.%s' % ext)
        output = os.sep.join(output)
        # todo could this be variabled?
        url_path = url_path.replace('.html', '/')

    output_dir = os.path.dirname(output)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not use_index_paths and path.endswith('index.html'):
        path = path.replace('index.html', '')

    request = urllib2.Request('%s/%s' % (url, path.replace(os.sep, '/')))
    request.add_header('X-Generate', '1')
    response = urllib2.urlopen(request).read()

    current_hash = None
    if os.path.exists(output):

        with open(output, 'r') as f:
            current_hash = hashlib.sha1(f.read()).hexdigest()

    if not current_hash or current_hash and current_hash != hashlib.sha1(response).hexdigest():
        with open(output, 'w') as f:
            f.write(response)
            print 'Generated %s' % output

    return url_path


sitemap_xml = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
sitemap_format = """
    <url>
      <loc>{0}</loc>
      <priority>0.5</priority>
    </url>
"""

for r, d, f in os.walk(template_path):
    for files in f:
        if files.endswith('html'):
            p = generate(os.path.join(r, files).replace(template_path + os.sep, ''))

            if sitemap and p:
                sitemap_xml += sitemap_format.format('{0}/{1}'.format(sitemap, p))

# write sitemap if modified
if sitemap:
    # close it
    sitemap_xml += '</urlset>'

    sitemap_path = os.path.join(output_path, 'sitemap.xml')
    current_hash = None

    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r') as f:
            current_hash = hashlib.sha1(f.read()).hexdigest()

    if not current_hash or current_hash and current_hash != hashlib.sha1(sitemap_xml).hexdigest():
        with open(sitemap_path, 'w') as f:
            f.write(sitemap_xml)
            print 'Generated %s' % sitemap_path