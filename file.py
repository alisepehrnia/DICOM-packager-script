import os
from zipfile import ZipFile, ZIP_DEFLATED

import consts

def get_dir_files(dir_path:str, extension_filter:str = None):
    list = []
    for root, _, files in os.walk(dir_path):
            for filename in files:
                if ((extension_filter != None and filename.endswith(extension_filter)) or
                    (extension_filter == None and filename.count('.') <= 0)):
                    list.append(os.path.join(root, filename))
    return list

def zip_dir(dir_path:str, zip_path:str, extension_filter:str = None):
    zip = ZipFile(zip_path, "w", ZIP_DEFLATED)
    files = get_dir_files(dir_path, extension_filter)
    num = 1
    for file in files:
        zip.write(file, f'{num}.{consts.processed_dicom_extension}')
        num += 1
    zip.close()

def create_yaml(tags_dict:dict, path:str=None, condition:bool = True):
    lines = ['---\n']
    for k, v in tags_dict.items():
        try:
            if (condition):
                lines.append(f"{k}: '{v}'\n")
        except:
            continue
    lines.append('...')
    return lines

def write_lines(lines:list[str], path:str):
    with open(path, "w") as f:
            f.writelines(lines)