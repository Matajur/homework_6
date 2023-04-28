from pathlib import Path
import shutil
import sys
import sort as parser
from normalize import normalize

# main logic


def handle_media(filename: Path, target_folder: Path) -> None:
    # create folder for media files
    target_folder.mkdir(exist_ok=True, parents=True)
    # move files there
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    # create folder for unknown files
    target_folder.mkdir(exist_ok=True, parents=True)
    # move files there
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    # create folder for archives
    target_folder.mkdir(exist_ok=True, parents=True)
    # create name for folder with archive's name
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    # create folder with archive's name
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        # unpack archive to the folder with atchive's name
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        folder_for_file.rmdir()     # folder removal if unpacking faled
        return None
    filename.unlink()               # archive removal


def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()              # folder removal
    except OSError:                 # an error if the folder cannot be removed
        print(f'Sorry, cannot be deleted the folder: {folder}')


def main(folder: Path) -> None:
    parser.scan(folder)
    for file in parser.JPEG_IMAGES + parser.JPG_IMAGES + parser.PNG_IMAGES + parser.SVG_IMAGES:
        handle_media(file, folder / 'images')
    for file in parser.MP3_AUDIO + parser.OGG_AUDIO + parser.WAV_AUDIO + parser.AMR_AUDIO:
        handle_media(file, folder / 'audio')
    for file in parser.AVI_VIDEO + parser.MP4_VIDEO + parser.MOV_VIDEO + parser.MKV_VIDEO:
        handle_media(file, folder / 'video')
    for file in parser.DOC_DOCS + parser.DOCX_DOCS + parser.TXT_DOCS + parser.PDF_DOCS + parser.XLSX_DOCS + parser.PPTX_DOCS:
        handle_media(file, folder / 'documents')

    for file in parser.OTHERS:
        handle_other(file, folder / 'other')

    for file in parser.ZIP_ARCHIVES + parser.GZ_ARCHIVES + parser.TAR_ARCHIVES:
        handle_archive(file, folder / 'archives')

    # reverse of folders to remove subfolders first
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == '__main__':
    folder_for_scan = Path(sys.argv[1])
    main(folder_for_scan.resolve())
