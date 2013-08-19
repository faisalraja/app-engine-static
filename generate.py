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

url = 'http://localhost:8080/dev'
template_path = 'templates'
output_path = 'gen'

if not os.path.exists(output_path):
    os.makedirs(output_path)


def generate(path):
    # Skips all layouts
    if path.startswith('layout'):
        return

    output = os.path.join(output_path, path)

    if hide_html_ext and not output.endswith('index.html'):
        output = output.split(os.sep)
        file = output.pop().split('.')
        ext = file.pop()
        output.append('.'.join(file))
        output.append('index.%s' % ext)
        output = os.sep.join(output)

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


for r, d, f in os.walk(template_path):
    for files in f:
        if files.endswith('html'):
            generate(os.path.join(r, files).replace(template_path + os.sep, ''))
