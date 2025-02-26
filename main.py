#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import shutil
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class mangaDownloader:
    def __init__(self, link, baseFolder):
        self.link = link
        self.baseFolder = os.getcwd() if len(baseFolder) == 0 else baseFolder
        self.MainResponse = requests.get(link)
        self.MainSoup = BeautifulSoup(self.MainResponse.text, 'html.parser')
        self.chapterDetails = self.MainSoup.find_all('li', {'class': "wp-manga-chapter"})
        self.allFolders = []

    def makeFolders(self):
        for chap_name in self.chapterDetails:
            self.makeFolder(chap_name)
    def makeFolder(self,chap_name):
        try:
            chapter_dir = chap_name.find('a', href=True, text=True).get_text()
        except:
            chapter_dir = (chap_name.find('a').get_text().strip())

        dir_name = os.path.join(self.baseFolder, chapter_dir.strip())
        if os.path.exists(dir_name):
            if os.listdir(dir_name):
                return "EXIST"

        print("creating:" + dir_name)
        os.makedirs(dir_name, exist_ok=True)
        self.allFolders.append(dir_name)
        return dir_name

    def downloadImagesInFolder(self):
        i = 0
        for curr_chap in self.chapterDetails:
            current_folder=self.makeFolder(curr_chap)
            if not current_folder == "EXIST":
                curr_link = curr_chap.find('a', href=True)['href']
                curr_chap_link_response = requests.get(curr_link)
                curr_chap_soup = BeautifulSoup(curr_chap_link_response.text, 'html.parser')
                img_tag = curr_chap_soup.find_all('img', {'class': "wp-manga-chapter-img"})
                all_images = [img['data-src'].strip() for img in img_tag]  # For current chapter

                for curr_img in all_images:
                    file_name = os.path.splitext(curr_img)[0].split("/")[-1]
                    file_ext = os.path.splitext(curr_img)[-1]
                    if os.path.exists(os.path.join(current_folder, f'{file_name}{file_ext}')):
                        print(f"Skipping file: {file_name}{file_ext} in Directory: {self.allFolders[i]}")
                        continue
                    page = requests.get(curr_img)
                    print(f"{bcolors.OKGREEN}Creating file: {file_name}{file_ext} in Directory: {current_folder}{bcolors.ENDC}")
                    with open(os.path.join(current_folder, f'{file_name}{file_ext}'), 'wb') as f:
                        f.write(page.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",help="manga url")
    parser.add_argument("-d","--dir",help="output directory")
    args = parser.parse_args()
    site = args.url
    inp_location = args.dir

    mangaDownloaderObj = mangaDownloader(site, inp_location)
    mangaDownloaderObj.downloadImagesInFolder()
