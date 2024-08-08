from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os 
import concurrent.futures

def authenticate(loc="credentials.txt", force_reload = False):
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile(loc)
    if (gauth.credentials is None):
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(loc)
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive


def list_folder(folder_id, drive):
    file_list = drive.ListFile({
        'q': "'%s' in parents" % folder_id,
        'supportsAllDrives': True,  # Modified
        'includeItemsFromAllDrives': True,  # Added
    }).GetList()

    return file_list 

def download_multiple_gdrive(file_list, local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    def download_file(download_inp):
        local_filepath, file_gd = download_inp
        if not os.path.exists(local_filepath):
            file_gd.GetContentFile(local_filepath)
            return 'Success: '+ str(local_filepath) + ' ' + str(len(os.listdir(local_dir)))
        else:
            return 'File already exists: {}'.format(local_filepath)

    thread_inps = [(local_dir + file['title'], file) for file in file_list]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for inp in thread_inps:
            futures.append(executor.submit(download_file, download_inp=inp))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())



# T1 MAT has more files
# id_ONDRI_T1_MAT = '1igfH8rY_6kMoQu5r8cGn7pX_MuKZg7mx'
# id_ONDRI_FLAIR_MAT = '1B_T4Hjv-EUfAbdpRmhJadaAzuN-2w6oM'
# id_ONDRI_MASK_MAT = '1PySprRjLV9lxNwCTxb8Vtp1EffqQkQ3b'#'138f8ct8btXgZllOPhWB7tUSO0SHBXI3F'
# id_ONDRI_FLAIR_STANDARDIZED_MAT = '1-cE3Q_nsy9CTg_HFGu9GAfDz9FguOPBQ'