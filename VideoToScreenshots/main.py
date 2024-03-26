from multiprocessing import Process
from VideoProcess import do_video_scrrenshot_process
import os

def _get_all_video_paths(folder_path='/Users/chunghanhsin/Documents/VideoToScreenshots/videos'):
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.mkv')]

    return file_paths



SRC_FOLDER_PATH = '/Users/chunghanhsin/Documents/TestEssential'
if __name__ == '__main__':
    # make_essential_developers_screen_shot()
    do_video_scrrenshot_process(SRC_FOLDER_PATH)