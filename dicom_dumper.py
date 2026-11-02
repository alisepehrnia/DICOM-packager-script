import json
from pydicom import FileDataset

def dump_tags(fileDataset: FileDataset, path:str = None):
    lines = []
    fileDataset.to_json
    for v in fileDataset.values():
        lines.append(str(v) + "\n")
    if (path != None):
        with open(path, "w") as f:
            f.writelines(lines)
    return lines

def dump_tags_json(fileDataset: FileDataset, path:str = None):
    json = fileDataset.to_json(dump_handler=json_dumper)
    if (path != None):
        with open(path, "w") as f:
            f.write(json)
    return json

def json_dumper(data):
    return json.dumps(data, indent=2, sort_keys=False)