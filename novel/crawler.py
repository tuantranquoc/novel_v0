from .models import Novel, Category, Chapter, Driver
from bs4 import BeautifulSoup
import requests
from slugify import slugify
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

PATH = 'C:\Program Files (x86)\chromedriver.exe'


def craw(href):
    url = 'https://metruyenchu.com/truyen/'
    # href = 'https://metruyenchu.com/truyen/vo-dich-chi-manh-nhat-than-cap-lua-chon'
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')

    # d-inline-block border border-success px-3 py-1 text-success rounded-3 mr-2 mb-2
    # d-inline-block border border-danger
    description_scrap = soup.find(class_="content")
    title = soup.find(class_="h3 mr-2")
    category = soup.find_all(
        class_="d-inline-block border border-success px-3 py-1 text-success rounded-3 mr-2 mb-2")
    category_01 = soup.find_all(
        class_="d-inline-block border border-primary px-3 py-1 text-primary rounded-3 mr-2 mb-2")
    status = soup.find(
        class_="d-inline-block border border-danger px-3 py-1 text-danger rounded-3 mr-2 mb-2")
    if status:
        if "Đang ra" in status.text:
            status = 1
        else:
            status = 2
    access_bar = soup.find_all(class_="font-weight-semibold h4 mb-1")
    number_of_chapter = 0
    chapter_per_week = 0
    bookmark_count = 0
    count = 0
    if title:
        slug = slugify(title.text)
        print("new novel: ", title.text)

        url += slug
    if title:
        if not Novel.objects.filter(title=title.text).first():
            if access_bar:
                for a in access_bar:
                    if count == 0:
                        number_of_chapter = a.text
                    elif count == 1:
                        chapter_per_week = a.text
                    elif count == 2:
                        view_count = a.text
                    elif count == 3:
                        bookmark_count = a.text
                    count += 1

            Novel.objects.create(title=title.text, status=status, description=description_scrap.text, number_of_chapter=number_of_chapter,
                                 slug=slug, source=href, public=True)
    for c in category:
        if c.text:
            if not Category.objects.filter(name=c.text):
                Category.objects.create(name=c.text)
            novel = Novel.objects.filter(title=title.text).first()
            category = Category.objects.filter(name=c.text).first()
            novel.category.add(category)
    for c in category_01:
        if c.text:
            if not Category.objects.filter(name=c.text):
                Category.objects.create(name=c.text)
            novel = Novel.objects.filter(title=title.text).first()
            category = Category.objects.filter(name=c.text).first()
            novel.category.add(category)

    novels = Novel.objects.filter(title=title.text)
    count = 1
    while(count <= novel.number_of_chapter):
        novel_source = novel.source + "/chuong-" + str(count)
        page = requests.get(novel_source)
        soup = BeautifulSoup(page.content, 'html.parser')
        chapter_title = soup.find(class_="nh-read__title")
        if chapter_title:
            chapter_list = Chapter.objects.filter(novel=novel)
            chapter = Chapter.objects.filter(
                title=chapter_title_filter(chapter_title.text, 2), novel=novel).first()
            if not chapter:
                chapter_number = int(
                    re.search(r'\d+', chapter_title.text).group())
                chapter = Chapter.objects.create(
                    title=chapter_title_filter(chapter_title.text, 2), novel=novel, chapter_number=chapter_number)
            print("chapter title: ", chapter.title)
            craw_chapter(novel_source, chapter)
        count += 1

    print("chapter-count: ", novel.number_of_chapter)
    print("Craw novel ", novel.title, " Done")
    print("--------------------------------------")


def craw_chapter(href, chapter):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(class_="nh-read__content post-body")
    if content:
        chapter.content = content.text
        chapter.save()


def get_url_from_main_page(href):
    # cover-wrapper z-depth-1 hoverable
    print("0: Select to change driver path")
    print("1: https://metruyenchu.com")
    print("2: https://nuhiep.com")
    print("3: https://vtruyen.com")
    print("4: https://wikidich.com")
    print("5: https://bachngocsach.com")
    print("6: https://truyen.tangthuvien.vn")
    val = int(input("Select value of your chose!: "))
    href = "123456877"
    if not Driver.objects.first():
        Driver.objects.create(path=PATH)
    if val == 0:
        driver_path = Driver.objects.first()
        if driver_path:
            print("current path: ", driver_path.path)
        path = input(
            "Copy and parse your absolute path to chrome driver here! ")
        print()
        if driver_path:
            driver_path.path = path
            driver_path.save()
    if val == 4:
        get_url_from_main_page_01()
    elif val == 1:
        href = "https://metruyenchu.com"
        main_function(href)
    elif val == 2:
        href = "https://nuhiep.com"
        main_function(href)
    elif val == 3:
        href = "https://vtruyen.com"
        main_function(href)
    elif val == 5:
        href = "https://bachngocsach.com"
        get_novel_link_from_main_page(href)
    elif val == 6:
        href = "https://truyen.tangthuvien.vn"
        get_novel_link_from_main_page_01(href)


def main_function(href):
    print(href)
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    novel_source = soup.find_all(class_="fz-body m-0 text-overflow-1-lines")
    novel_source_01 = soup.find_all("a", class_="d-block")
    if novel_source:
        for n in novel_source:
            children = n.findChildren("a", recursive=True)
            for c in children:
                href = c.get('href')
                craw(href)
    if novel_source_01:
        for n in novel_source_01:
            href = n.get('href')
            if "pub.truyen.onl" in href:
                continue
            craw(href)


def chapter_title_filter(title, number):
    arr = title.split()
    count = 1
    while count <= number:
        arr.pop(0)
        count += 1
    listToStr = ' '.join(map(str, arr))
    return listToStr


def craw_01(href):
    path = PATH
    if Driver.objects.first():
        path = Driver.objects.first().path
    driver = webdriver.Chrome(path)
    url = 'https://wikidich.com/truyen/'
    main_url = 'https://wikidich.com'
    # href = 'https://wikidich.com/truyen/thinh-dinh-chi-nguoi-truong-tam-hanh-vi-YEfailS4CDHvEhMz'
    driver.get(href)
    respData = driver.page_source
    driver.quit()
    # page = requests.get(href)
    soup = BeautifulSoup(respData, 'html.parser')
    title = soup.find(
        'h2', style="font-size: 1.7rem; font-weight: bold; margin: 0; color: #444444")
    category = soup.findAll('span', style="color: #01bed6")
    description = soup.find(
        'div', class_="book-desc-detail")
    access_bar = soup.find_all('p', style="margin: 0.9rem 0")

    chapter_link = soup.find_all('li', class_="chapter-name")
    for i in range(len(access_bar)):
        if i == 2:
            status = access_bar[i].text
            if 'Còn tiếp' in status:
                status = 1
            else:
                status = 2

    if description:
        description = description.text
    else:
        description = ""
    slug = href.replace('https://wikidich.com/truyen/', '')
    url += slug
    if title:
        if not Novel.objects.filter(title=title.text).first():
            Novel.objects.create(title=title.text, status=status,
                                 description=description, slug=slug, source=url, public=True)

    for c in category:
        children = c.findChildren("a", recursive=False)
        for child in children:
            # print(child.text)
            if not Category.objects.filter(name=child.text):
                Category.objects.create(name=child.text)
            novel = Novel.objects.filter(title=title.text).first()
            category = Category.objects.filter(name=child.text).first()
            novel.category.add(category)
    if title:
        print("New novel: ", title.text)
        novel = Novel.objects.filter(title=title.text).first()
        count = 1
        if chapter_link:
            for chapter in chapter_link:
                children = chapter.findChildren("a", recursive=True)
                for c in children:
                    href = c.get('href')
                    chapter_source = main_url + href
                    craw_chapter_01(chapter_source, novel, count)
                    count = count + 1
        count_ = Chapter.objects.filter(novel=novel).count()
        print("total chapter craw: ", count_)
        novel.number_of_chapter = count_
        novel.save()
        print("Craw chapters - done")
        print("--------------------------------------")


def craw_chapter_01(href, novel, chapter_number):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    chapter_title = soup.find_all('p', class_="book-title")
    content = soup.find('div', id="bookContentBody")
    count = 0
    title = ""
    chapter_number = ""

    if chapter_title:
        for c in chapter_title:
            if count == 1:
                title = c.text
            count += 1
        chapter = Chapter.objects.filter(
            title=c.text, novel=novel).first()
        if not chapter:
            print("chapter title: ", title)
            chapter = Chapter.objects.create(
                title=title, novel=novel, chapter_number=chapter_number, content=content.text)


def get_url_from_main_page_01():
    href = "https://wikidich.com"
    path = PATH
    if Driver.objects.first():
        path = Driver.objects.first().path
    driver = webdriver.Chrome(path)
    print(href)
    driver.get(href)
    respData = driver.page_source
    driver.quit()
    # page = requests.get(href)
    soup = BeautifulSoup(respData, 'html.parser')
    novel_links = soup.find_all(
        'a', class_="cover-wrapper z-depth-1 hoverable")
    if novel_links:
        for n in novel_links:
            novel_source = href + n.get('href')
            craw_01(novel_source)


def get_novel_link_from_main_page(href):
    print(href)
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    novel_links = soup.find_all("a", class_="recent-anhbia-a")
    for n in novel_links:
        href = n.get('href')
        # print(href)
        craw_02(href)


def craw_02(href):
    url = 'https://bachngocsach.com'
    # href = 'https://bachngocsach.com/reader/lam'
    page = requests.get(url + href)
    soup = BeautifulSoup(page.content, 'html.parser')
    description = soup.find(
        'div', id="gioithieu")
    categories = soup.find_all(
        'div', id="theloai")
    title = soup.find(
        'h1', id="truyen-title")

    if description:
        description = description.text
    else:
        description = ""
    slug = href.replace('https://bachngocsach.com', '')
    source = url + slug
    if title:
        if not Novel.objects.filter(title=title.text).first():
            Novel.objects.create(title=title.text,
                                 description=description, slug=slug, source=source, public=True)

    if categories:
        for category in categories:
            children = category.findChildren("a", recursive=True)
            for c in children:
                if not Category.objects.filter(name=c.text):
                    Category.objects.create(name=c.text)
                novel = Novel.objects.filter(title=title.text).first()
                category = Category.objects.filter(name=c.text).first()
                novel.category.add(category)
    if title:
        novel = Novel.objects.filter(title=title.text).first()
        table_of_contents = source + "/" + "muc-luc"
        # print("current link " + table_of_contents)
        get_chapter(table_of_contents, novel, url)


def get_chapter(href, novel, url):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    chapter_links = soup.find_all("div", class_="mucluc-chuong")
    if chapter_links:
        for c in chapter_links:
            children = c.findChildren("a", recursive=True)
            for c in children:
                href = c.get('href')
                href = url + "/" + href
                craw_chapter_03(href, novel)


def craw_chapter_03(href, novel):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("h1", id="chuong-title")
    content = soup.find("div", id="noi-dung")
    if title:
        print("chapter_title: ", title.text)
        try:
            chapter_number = int(
                re.search(r'\d+', title.text).group())
        except:
            chapter_number = None
        title = chapter_title_filter(title.text, 2)
        if not Chapter.objects.filter(title=title, novel=novel):
            if content:
                Chapter.objects.create(
                    title=title, content=content.text, novel=novel, chapter_number=chapter_number)


def get_novel_link_from_main_page_01(href):
    print(href)
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    novel_links = soup.find_all("a", class_="name")
    novel_links_01 = soup.find_all("h3")
    if novel_links:
        for n in novel_links:
            href = n.get('href')
            # print(href)
            craw_03(href)
        print("=================================")
    if novel_links_01:
        for n in novel_links_01:
            children = n.findChildren("a", recursive=False)
            for c in children:
                href = c.get('href')
                if "javascript" in href:
                    continue
                # print(href)
                craw_03(href)
        print("=================================")


def craw_03(href):
    url = 'https://truyen.tangthuvien.vn'
    # href = 'https://bachngocsach.com/reader/lam'
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    category = soup.find("a", class_="red")
    status = soup.find("span", class_="blue")
    number_of_chapter = soup.find("a", id="j-bookCatalogPage")
    description = soup.find(
        'div', class_="book-intro")
    categories = soup.find_all(
        'div', id="theloai")
    title = soup.find(
        'h1')
    count = 0
    if status:
        if status.text == "Đã hoàn thành":
            status = 2
        else:
            status = 1
    # if title:
    #     print(title.text)

    if description:
        description = description.text
    else:
        description = ""
    slug = href.replace('https://truyen.tangthuvien.vn', '')
    source = url + slug

    # print(slug)
    if title:
        if not Novel.objects.filter(title=title.text).first():
            Novel.objects.create(title=title.text,
                                 description=description, slug=slug, source=source, public=True)

    if categories:
        for category in categories:
            children = category.findChildren("a", recursive=True)
            for c in children:
                if not Category.objects.filter(name=c.text):
                    Category.objects.create(name=c.text)
                novel = Novel.objects.filter(title=title.text).first()
                category = Category.objects.filter(name=c.text).first()
                novel.category.add(category)
    if title:
        print("New novel: ", title.text)
        novel = Novel.objects.filter(title=title.text).first()
        if number_of_chapter:
            try:
                number_of_chapter = re.search(
                    r'\d+', number_of_chapter.text).group()
                print("Number of chapter: ", number_of_chapter)
                novel.number_of_chapter = number_of_chapter
                novel.save()
                print(href)
            except:
                number_of_chapter = 0
            index = 1
            while(index <= int(number_of_chapter)):
                chapter_source = href + "/" + "chuong-" + str(index)
                # print("chapter-source ", chapter_source)
                get_chapter_03(chapter_source, novel, index)
                index += 1


def get_chapter_03(href, novel, chapter_number):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')

    chapter_title = soup.find("h2")
    content_list = soup.find_all("div", class_="box-chap")
    content = ""
    if content_list:
        for c in content_list:
            content += c.text
    if chapter_title:
        print(chapter_title.text)
        chapter_title = chapter_title_filter(chapter_title.text, 3)
        if not Chapter.objects.filter(title=chapter_title, novel=novel):
            if content:
                Chapter.objects.create(
                    title=chapter_title, content=content, novel=novel, chapter_number=chapter_number)
