import sys
from pathlib import Path

# sorting according to file extension

JPEG_IMAGES, JPG_IMAGES, PNG_IMAGES, SVG_IMAGES = [], [], [], []    # lists of images

MP3_AUDIO, OGG_AUDIO, WAV_AUDIO, AMR_AUDIO = [], [], [], []         # audio lists

AVI_VIDEO, MP4_VIDEO, MOV_VIDEO, MKV_VIDEO = [], [], [], []         # video lists

DOC_DOCS, DOCX_DOCS, TXT_DOCS, PDF_DOCS, XLSX_DOCS, PPTX_DOCS = [
], [], [], [], [], []                                               # documents

ZIP_ARCHIVES, GZ_ARCHIVES, TAR_ARCHIVES = [], [], []            # lists of archives

OTHERS = []                                                 # unknown extensions

REGISTER_EXTENSION = {
    'jpeg': JPEG_IMAGES, 'jpg': JPG_IMAGES, 'png': PNG_IMAGES, 'svg': SVG_IMAGES,
    'avi': AVI_VIDEO, 'mp4': MP4_VIDEO, 'mov': MOV_VIDEO, 'mkv': MKV_VIDEO,
    'mp3': MP3_AUDIO, 'ogg': OGG_AUDIO, 'wav': WAV_AUDIO, 'amr': AMR_AUDIO,
    'doc': DOC_DOCS, 'docx': DOCX_DOCS, 'txt': TXT_DOCS, 'pdf': PDF_DOCS, 'xlsx': XLSX_DOCS, 'pptx': PPTX_DOCS,
    'zip': ZIP_ARCHIVES, 'gz': GZ_ARCHIVES, 'tar': TAR_ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()
FOLDERS_TO_IGNORE = ('archives', 'video', 'audio',
                     'documents', 'images', 'other')    # the folders to collect files according to extension


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].lower()


def scan(folder: Path):
    for item in folder.iterdir():
        # Folder's processing
        if item.is_dir():
            # check if the folder is not final storage for files
            if item.name not in FOLDERS_TO_IGNORE:
                FOLDERS.append(item)
                scan(item)              # scan subfolder - recursion
            continue                    # pass to next item if the folder to ignore
        # File's processing
        ext = get_extension(item.name)  # get extension of the file
        full_name = folder / item.name  # get full path to the file
        if not ext:
            OTHERS.append(full_name)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSIONS.add(ext)
                container.append(full_name)
            except KeyError:            # KeyError if the key is not present in the dictionary
                UNKNOWN.add(ext)
                OTHERS.append(full_name)


if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder: {folder_for_scan}')

    scan(Path(folder_for_scan))
    for extension, files in REGISTER_EXTENSION.items():
        print(f'Files {extension}: {files}')
    print(f'Files unknown: {OTHERS}')
    print('*' * 25)
    print(f'Types of file in folder: {EXTENSIONS}')
    print(f'Unknown types of file: {UNKNOWN}')
    print(f'List of folders: {FOLDERS}')
