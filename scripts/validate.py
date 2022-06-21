import json
import os
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

def main():
    failed = 0
    f = open('../schema/schema.json')
    schema = json.load(f)
    """
    Validate json files in db directory and all subdirectories recursively
    """
    for root, dirs, files in os.walk('../db'):
        for file in files:
            if file.endswith('.json'):
                filename = os.path.join(root, file)
                try:
                    with open(filename) as f:
                        data = json.load(f)
                        validate(data, schema)
                except ValidationError as e:
                    failed = 1
                    print('ValidationError in file: ' + filename, file=sys.stderr)
                    print(e, file=sys.stderr)
                    pass
                except SchemaError as e:
                    failed = 1
                    print('SchemaError in file: ' + filename, file=sys.stderr)
                    print(e, file=sys.stderr)
                    pass
    f.close()
    if failed:
        print('Validation completed with errors', file=sys.stderr)
        sys.exit(1)
    print('Validation completed successfully')

if __name__ == '__main__':
    main()