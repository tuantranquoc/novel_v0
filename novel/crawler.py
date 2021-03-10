from .models import Novel, Category, Chapter
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
    view_count = "0k"
    bookmark_count = 0
    count = 0
    if title:
        slug = slugify(title.text)
        print(title.text)

        url += slug
    print(url)
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
            print("new novel: ", title.text)
            Novel.objects.create(title=title.text, status=status, description=description_scrap.text, number_of_chapter=number_of_chapter,
                                 view_count=view_count, slug=slug, source=url, public=True)
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
    while(count <= 10):
        novel_source = novel.source + "/chuong-" + str(count)
        page = requests.get(novel_source)
        soup = BeautifulSoup(page.content, 'html.parser')
        chapter_title = soup.find(class_="nh-read__title")
        if chapter_title:
            chapter_list = Chapter.objects.filter(novel=novel)
            chapter = Chapter.objects.filter(
                title=chapter_title_filter(chapter_title.text), novel=novel).first()
            if not chapter:
                chapter_number = int(
                    re.search(r'\d+', chapter_title.text).group())
                chapter = Chapter.objects.create(
                    title=chapter_title_filter(chapter_title.text), novel=novel, chapter_number=chapter_number)
            print(chapter.title)
            craw_chapter(novel_source, chapter)
        count += 1
    print("Craw 10 chapters - done")
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
    print("1: https://metruyenchu.com")
    print("2: https://nuhiep.com")
    print("3: https://vtruyen.com")
    print("4: https://wikidich.com")
    val = int(input("Select value of your chose!: "))
    href = "123456877"
    print()
    if val == 4:
        get_url_from_main_page_01()
    elif val == 1:
        href = "https://metruyenchu.com"
        print(href)
        main_function(href)
    elif val == 2:
        href = "https://nuhiep.com"
        main_function(href)
    elif val == 3:
        href = "https://vtruyen.com"
        main_function(href)


def main_function(href):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    title_list = soup.find_all(class_="fz-body m-0 text-overflow-1-lines")
    for title in title_list:
        children = title.findChildren("a", recursive=True)
        for c in children:
            href = c.get('href')
            craw(href)


def chapter_title_filter(title):
    arr = title.split()
    arr.pop(0)
    arr.pop(0)
    listToStr = ' '.join(map(str, arr))
    return listToStr


def craw_01(href):
    driver = webdriver.Chrome(PATH)
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
        print(access_bar[i].text)
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
        print("Craw 10 chapters - done")
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
            chapter = Chapter.objects.create(
                title=title, novel=novel, chapter_number=chapter_number, content=content.text)


def get_url_from_main_page_01():
    href = "https://wikidich.com"
    driver = webdriver.Chrome(PATH)
    print(href)
    driver.get(href)
    respData = driver.page_source
    # driver.quit()
    # page = requests.get(href)
    soup = BeautifulSoup(respData, 'html.parser')
    novel_links = soup.find_all(
        'a', class_="cover-wrapper z-depth-1 hoverable")
    if novel_links:
        for n in novel_links:
            novel_source = href + n.get('href')
            print(novel_source)
            craw_01(novel_source)
    if not novel_links:
        print("hopeless")
