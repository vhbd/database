import json
import errno
import os
import sys

# From https://gist.github.com/KinoAR/a5cf8a207529ee643389c4462ebf13cd
def minify(file_name):
    file_data = open(file_name, "r", 1).read()
    json_data = json.loads(file_data)
    json_string = json.dumps(json_data, separators=(',', ":"))
    file_name = str(file_name).replace(".json", "")
    new_file_name = "{0}_minify.json".format(file_name)
    open(new_file_name, "w+", 1).write(json_string)

def main():
    homebrew = ''
    plugins = ''

    try:
        os.mkdir('../out', )
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    for root, dirs, files in os.walk('../db/apps'):
        for file in files:
            if file.endswith('.json'):
                filename = os.path.join(root, file)
                with open(filename) as f:
                    text = f.read()
                    homebrew = homebrew + text + ',\n'
    homebrew = '[\n' + homebrew.rstrip(',\n') + '\n]'
    with open('../out/db_homebrew.json', 'w') as f:
        f.write(homebrew)

    for root, dirs, files in os.walk('../db/plugins'):
        for file in files:
            if file.endswith('.json'):
                filename = os.path.join(root, file)
                with open(filename) as f:
                    text = f.read()
                    plugins = plugins + text + ',\n'
    plugins = '[\n' + plugins.rstrip(',\n') + '\n]'
    with open('../out/db_plugins.json', 'w') as f:
        f.write(plugins)

    with open('../out/db.json', 'w') as f:
        f.write('{\n"homebrew":\n' + homebrew +',\n"plugins":\n' + plugins + '\n}')
    minify('../out/db.json')


if __name__ == '__main__':
    main()