#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:09:53 2021

@author: asrock
"""

import time
import numpy.random as random 
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import glob, os, os.path as path 
import pyautogui
import shutil
import cv2


def run_image_scrap(names, n_imgs, savefolder, chrome_driver):
    if not os.path.exists(savefolder): 
        os.mkdir(savefolder)
    for idx, file_path in enumerate(names):
        try:
            with webdriver.Chrome(chrome_driver) as driver:
                print('image: %d'%idx)
                names = cv2.imread(file_path)
                s_folder = path.join(savefolder, '%d/'%(idx))
                if not path.exists(s_folder): 
                    os.mkdir(s_folder)

                driver.get("https://www.bing.com/?scope=images&nr=1&FORM=NOFORM")
                time.sleep(2)

                #find image search icon
                search_by_image_btn = driver.find_elements_by_xpath("//div[@id='sb_sbip']")[0]
                search_by_image_btn.click()
                
                #upload image
                choose_file_btn = driver.find_elements_by_xpath('//input[@id="sb_fileinput"]')[0]
                choose_file_btn.send_keys(file_path)

                #wait for the seed image to upload
                time.sleep(10)

                #locate "search for similar image" botton
                if driver.find_elements_by_xpath("//span[@data-tooltip='See more images']/span[2]"):
                    visually_similar_images = driver.find_elements_by_xpath("//span[@data-tooltip='See more images']/span[2]")[0]
                
                    visually_similar_images.click()
                default_savefolder = path.join(path.expanduser('~'), 'Downloads/*')
                exists = glob.glob(default_savefolder)

                count = 0
                track = 0
                
                flag = 0
                while count <= n_imgs:
                    elements = driver.find_elements_by_class_name('richImgLnk')
                    if not elements or track>= len(elements)-1:
                        flag = 1
                        break
                    #open the returned images one by one
                    element = driver.find_elements_by_class_name('richImgLnk')[track]
                    element.click()
                    time.sleep(1)
                    
                    #find the big image
                    big_img = driver.find_elements_by_class_name('nofocus')[2]
                    if big_img.get_attribute("src"):
                        time.sleep(1.5)
                        #right click
                        webdriver.ActionChains(driver).context_click(big_img).perform()
                        time.sleep(1.5)
                        # "save as"
                        pyautogui.press('v')
                        time.sleep(3)
                        #press "enter" to save
                        pyautogui.press('enter')

                        count += 1
                        track += 1
                    close = driver.find_elements_by_xpath("//div[@name='Close image']")[0]
                    close.click()
                    time.sleep(random.uniform(0.5,1))
                newfiles = glob.glob(default_savefolder)
                for file in newfiles: 
                    if file not in exists: #find the newly scrapped image  
                        shutil.move(file, s_folder)
        except:
            pass
            
if __name__=='__main__': 
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, type=str, help="folder to store all seed images")
    ap.add_argument("-o", "--output", required=True, type=str, help="folder to store scrapped images")
    ap.add_argument("-n", "--n_image", default=30, type=int, help="# of images expected from each seed")
    ap.add_argument("-c", "--chrome_driver", default='./chromedriver_92', type=str, help="folder to store scrapped images")
    args = vars(ap.parse_args())
    
    names = glob.glob(path.join(args.folder, '*.jpg'))
    names += glob.glob(path.join(args.folder, '*.JPG'))
    names += glob.glob(path.join(args.folder, '*.JPEG'))
    names += glob.glob(path.join(args.folder, '*.png'))
    
    n_imgs = args.n_image
    savefolder = args.output
    chrome_driver = args.chrome_driver
    run_image_scrap(names, n_imgs, savefolder, chrome_driver) 