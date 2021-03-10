from .models import Novel, Category, Chapter
from bs4 import BeautifulSoup
import requests
from slugify import slugify
import re


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
    href_list = ("https://metruyenchu.com",
                 "https://nuhiep.com/", "https://vtruyen.com")
    for href in href_list:
        print(href)
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
