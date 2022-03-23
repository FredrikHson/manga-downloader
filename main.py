#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import shutil
import argparse




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
            try:
                chapter_dir = chap_name.find('a', href=True, text=True).get_text()
            except:
                chapter_dir = (chap_name.find('a').get_text().strip())

            dir_name = os.path.join(self.baseFolder, chapter_dir.strip())
            if os.path.exists(dir_name):
                print(f"Reusing {dir_name}")
                # shutil.rmtree(dir_name)
            else:
                pass
            os.makedirs(dir_name, exist_ok=True)
            self.allFolders.append(dir_name)

    def downloadImagesInFolder(self):
        i = 0
        for curr_chap in self.chapterDetails:
            curr_link = curr_chap.find('a', href=True)['href']
            curr_chap_link_response = requests.get(curr_link)
            curr_chap_soup = BeautifulSoup(curr_chap_link_response.text, 'html.parser')
            img_tag = curr_chap_soup.find_all('img', {'class': "wp-manga-chapter-img"})
            all_images = [img['data-src'].strip() for img in img_tag]  # For current chapter

            for curr_img in all_images:
                file_name = os.path.splitext(curr_img)[0].split("/")[-1]
                file_ext = os.path.splitext(curr_img)[-1]
                if os.path.exists(os.path.join(self.allFolders[i], f'{file_name}{file_ext}')):
                    # print(f"Skipping file: {file_name}{file_ext} in Directory: {self.allFolders[i]}")
                    continue
                page = requests.get(curr_img)
                print(f"Creating file: {file_name}{file_ext} in Directory: {self.allFolders[i]}")
                with open(os.path.join(self.allFolders[i], f'{file_name}{file_ext}'), 'wb') as f:
                    f.write(page.content)
            i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--url",help="manga url")
    parser.add_argument("-d","--dir",help="output directory")
    args = parser.parse_args()
    site = args.url
    inp_location = args.dir

    mangaDownloaderObj = mangaDownloader(site, inp_location)
    mangaDownloaderObj.makeFolders()
    mangaDownloaderObj.downloadImagesInFolder()
