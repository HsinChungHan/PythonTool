from captions_manager import convert_all_srts
from translate_srt_manager import do_translation_process as do_translate_srts_process
from summary_manager import do_summary_srts_process
from translate_summary_manager import do_translate_process as do_translate_summary_process
import os
from convert_simplified_to_traditional_chinese import convert_under_folder
from essential_developer_manager import clean_vtt_files


BILINGUAL_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/bilingual_srts'
ARCHIVED_MERGED_CH_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/archived_merged_ch'

SPLITED_CH_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/splited_ch'

CH_SUMMARY_TEXTS = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/ch_summary_texts'

def _delete_empty_directories(directory):
    if not os.path.exists(directory):
        return 
    # Check if directory is empty
    if not os.listdir(directory):
        print(f'Deleting empty directory: {directory}')
        os.rmdir(directory)

    # Otherwise, if the directory is not empty, loop through and check all subdirectories
    else:
        for subdir in os.listdir(directory):
            full_subdir = os.path.join(directory, subdir)

            # If this directory contains further directories, recurse into those
            if os.path.isdir(full_subdir):
                _delete_empty_directories(full_subdir)

SPLITED_EN_FOLDER = '/Users/chunghanhsin/Desktop/YoutubeCaptionCrawler/translate_srt_manager/translation/splited_en'

if __name__ == "__main__":
    # _delete_empty_directories(SPLITED_EN_FOLDER)
    
    # convert_all_srts()
    # clean_vtt_files()
    do_translate_srts_process()
    # do_summary_srts_process()
    # do_translate_summary_process()  

    # convert_under_folder(BILINGUAL_SRTS_FOLDER)
    # convert_under_folder(CH_SUMMARY_TEXTS)
    # convert_under_folder(SPLITED_CH_FOLDER)
    # convert_under_folder(ARCHIVED_MERGED_CH_SRTS_FOLDER)
    
    