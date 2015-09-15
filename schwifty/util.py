import os

from schwifty.core import app


def angular_templates():
    partials_dir = os.path.join(app.static_folder, '..')
    partials_dir = os.path.join(partials_dir, 'templates', 'angular')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                file_name = file_path[len(partials_dir) + 1:]
                yield (file_name, fh.read().decode('utf-8'))
