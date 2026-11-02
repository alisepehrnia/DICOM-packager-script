from pydicom import FileDataset
from pydicom.uid import JPEGLSLossless, JPEGLSNearLossless

from file import create_yaml, write_lines

def process(dicom_ds:FileDataset,
            sensitive_tags_kws:list[str] = [],
            sensitive_tags_out_path:str = None,
            dump_tags_kws:list[str] = [],
            dump_tags_out_path:str = None,
            recompress:bool = True,
            compression_jls_err:int = 1,
            img_path:str = None):
    dicom_ds.remove_private_tags()
    # Get metadata
    p_name = safe_get_tag_val(dicom_ds, 'PatientName')
    p_id = safe_get_tag_val(dicom_ds, 'PatientID')
    # Save and remove sensitive tags
    save_remove_tags(dicom_ds, sensitive_tags_kws, remove=True, path=sensitive_tags_out_path)
    # Save useful tags
    save_remove_tags(dicom_ds, dump_tags_kws, remove=False, path=dump_tags_out_path)
    # Recompress
    if (recompress):
        if dicom_ds.file_meta.TransferSyntaxUID.is_compressed == True:
            dicom_ds.decompress()
        if (compression_jls_err == None):
            dicom_ds.compress(JPEGLSLossless)
        else:
            dicom_ds.compress(JPEGLSNearLossless, jls_error=compression_jls_err)

    if (img_path != None):
        dicom_ds.save_as(img_path, enforce_file_format=True)
    
    return type('',(),{'dicom_ds': dicom_ds, 'patient_name': p_name, 'patient_id': p_id})()

def dump_remove_tags(dicom_ds: FileDataset, tags_kws:list[str], remove:bool = False, path:str = None):
    tags = dict()
    for kw in tags_kws:
        try:
            tags[kw] = dicom_ds[kw].value
            if (remove): del dicom_ds[kw]
        except:
            continue
    return tags

def save_remove_tags(dicom_ds: FileDataset, tags_kws:list[str], remove:bool = False, path:str = None):
    tags_dict = dump_remove_tags(dicom_ds, tags_kws, remove, path)
    yaml_lines = create_yaml(tags_dict, path != None)
    if (path != None):
        write_lines(yaml_lines, path)
    return dicom_ds

def safe_get_tag_val(dicom_ds:FileDataset, tag_kw:str):
    try:
        return dicom_ds[tag_kw].value
    except:
        return None