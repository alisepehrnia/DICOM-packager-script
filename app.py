import os
import sys
from persiantools.jdatetime import JalaliDate
from pydicom import dcmread

from file import get_dir_files, zip_dir
from config import read_config
from dicom_processor import process
import consts

cfg = read_config()

pack_dir_name = cfg['pack_folder_name']
images_dir_path = sys.argv[1]
pack_path = f'{images_dir_path}/{pack_dir_name}'
pack_ext = cfg['pack_extension']
data_ext = cfg['data_extension']
imgs_ext = cfg['imagesExtension']
do_recompress = cfg['recompress']
compression_err = cfg['compression_jls_error']
sensitive_tags_kws = cfg['sensitive_tags_keywords']
dump_tags_kws = cfg['dump_tags_keywords']

if not os.path.exists(pack_path):
    os.makedirs(pack_path)

imgs = get_dir_files(images_dir_path, extension_filter=imgs_ext)
sensitive_tags_out_path = f'{pack_path}/sensitive.{pack_ext}'
dump_tags_out_path = f'{pack_path}/tags.{pack_ext}'
file_num = 1
for img in imgs:
    dicom_ds = dcmread(img)
    splitted_img_path = str.split(img,'\\')
    img_path = f'{''.join(splitted_img_path[:len(splitted_img_path) - 1])}/{pack_dir_name}/{file_num}.{consts.processed_dicom_extension}'
    process_res = process(dicom_ds,
                        sensitive_tags_kws,
                        sensitive_tags_out_path,
                        dump_tags_kws,
                        dump_tags_out_path,
                        recompress=do_recompress,
                        compression_jls_err=compression_err,
                        img_path=img_path)
    sensitive_tags_out_path = None
    file_num += 1
    if (process_res.patient_name != None and str(process_res.patient_name).strip()):
        zip_name = process_res.patient_name
    elif (process_res.patient_id != None and str(process_res.patient_id).strip()):
        zip_name = process_res.patient_id
    else:
        zip_name = 'samap_pack'
zip_dir(dir_path=pack_path,
        zip_path=f"{zip_name}_{JalaliDate.today().isoformat()}.{pack_ext}",
        extension_filter=consts.processed_dicom_extension)