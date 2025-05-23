import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
from datetime import datetime
import xml.etree.ElementTree as ET

BLOG_DIR = "blog"
INDEX_FILE = "index.html"
ACCORDION_ID = "blog-list"
BLOG_SECTION_ID = "blog"
SITEMAP_FILE = "sitemap.xml"
SITE_URL = "https://fastcredit.sk"

def extract_section_content(html_content, section_id):
    """Извлекает содержимое секции по её ID"""
    soup = BeautifulSoup(html_content, "html.parser")
    section = soup.find("section", {"id": section_id})
    return str(section).strip() if section else ""

def extract_article_info(filepath):
    """Извлекает информацию о статье из HTML файла"""
    # Получаем имя файла
    filename = os.path.basename(filepath)
    
    # Пропускаем файлы, начинающиеся с "ПРИМЕР"
    if filename.startswith("ПРИМЕР"):
        return None
    
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        
        # Извлекаем заголовок h1
        h1 = soup.find("h1")
        title = h1.text.strip() if h1 else ""
        
        # Если h1 пустой, берем из title
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.text.strip()
                # Убираем суффикс сайта если есть
                title = title.split(" | ")[0].strip()
            
        # Извлекаем описание (первый параграф после h1 или meta description)
        meta_desc = soup.find("meta", {"name": "description"})
        description = ""
        
        if meta_desc and meta_desc.get("content"):
            description = meta_desc["content"].strip()
        else:
            # Ищем первый параграф после h1
            if h1:
                next_p = h1.find_next_sibling("p")
                if next_p:
                    description = next_p.text.strip()[:200] + "..." if len(next_p.text) > 200 else next_p.text.strip()
        
        return {
            "title": title,
            "description": description,
            "filename": filename,
            "href": f"/blog/{filename}"
        }

def generate_blog_slider_html(articles):
    """Генерирует HTML для слайдера блога"""
    slides_html = ""
    
    for article in articles:
        slide = f'''                <div class="swiper-slide">
                  <a href="{article['href']}" class="blog-card">
                    <img
                      src="/assets/blog/b1.webp"
                      alt="articles"
                      loading="lazy"
                    />
                    <h3>{article['title']}</h3>
                    <p>{article['description']}</p>
                    <div class="blog-card-bottom">
                      <span>Podrobnosti →</span>
                    </div>
                  </a>
                </div>
'''
        slides_html += slide
    
    # Создаем полную секцию
    section_html = f'''      <section id="blog" class="blog-home">
        <div class="container">
          <h2>Náš blog</h2>
          <div class="blog-home__wrapper">
            <div class="swiper blogSwiper">
              <div class="swiper-wrapper">
{slides_html.rstrip()}
              </div>
              <div class="swiper-button-next"></div>
              <div class="swiper-button-prev"></div>
              <div class="swiper-pagination"></div>
            </div>
          </div>
        </div>
      </section>'''
    
    return section_html

def find_unique_section():
    """Находит уникальную секцию blog-list среди всех файлов блога"""
    content_map = defaultdict(list)
    
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".html"):
            path = os.path.join(BLOG_DIR, filename)
            with open(path, "r", encoding="utf-8") as file:
                html = file.read()
                section_html = extract_section_content(html, ACCORDION_ID)
                if section_html:
                    content_map[section_html].append(filename)

    if len(content_map) == 1:
        print("⚠️ Все секции blog-list одинаковые — нечего обновлять.")
        return None

    for content, files in content_map.items():
        if len(files) == 1:
            print(f"✅ Найдена уникальная секция blog-list в файле: {files[0]}")
            return content

    print("❌ Нет уникальной секции blog-list — либо все разные, либо повторяются по нескольку раз.")
    return None

def update_all_articles(new_section_html):
    """Обновляет секцию blog-list во всех файлах блога"""
    updated_count = 0
    
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".html"):
            path = os.path.join(BLOG_DIR, filename)
            with open(path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            old_section = soup.find("section", {"id": ACCORDION_ID})
            if old_section:
                new_section_soup = BeautifulSoup(new_section_html, "html.parser")
                old_section.replace_with(new_section_soup)
                
                with open(path, "w", encoding="utf-8") as file:
                    file.write(str(soup))
                updated_count += 1
    
    return updated_count

def update_index_blog_section():
    """Обновляет секцию блога в index.html на основе всех статей"""
    # Собираем информацию о всех статьях
    articles = []
    
    for filename in sorted(os.listdir(BLOG_DIR)):
        if filename.endswith(".html"):
            path = os.path.join(BLOG_DIR, filename)
            article_info = extract_article_info(path)
            if article_info:  # None если файл начинается с "ПРИМЕР"
                articles.append(article_info)
    
    if not articles:
        print("❌ Не найдено статей для обновления в index.html")
        return False
    
    # Генерируем новый HTML для секции блога
    new_blog_section = generate_blog_slider_html(articles)
    
    # Обновляем index.html
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
        
        old_section = soup.find("section", {"id": BLOG_SECTION_ID})
        if old_section:
            new_section_soup = BeautifulSoup(new_blog_section, "html.parser")
            old_section.replace_with(new_section_soup)
            
            with open(INDEX_FILE, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"✅ Обновлена секция блога в index.html ({len(articles)} статей)")
            return True
        else:
            print("❌ Не найдена секция блога в index.html")
            return False
            
    except FileNotFoundError:
        print(f"❌ Файл {INDEX_FILE} не найден")
        return False
    except Exception as e:
        print(f"❌ Ошибка при обновлении index.html: {e}")
        return False

def update_sitemap():
    """Обновляет sitemap.xml, добавляя новые статьи"""
    try:
        # Регистрируем namespace для корректной работы с XML
        ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        
        # Парсим существующий sitemap
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
        
        # Получаем namespace
        ns = {'': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Собираем существующие URL из sitemap
        existing_urls = set()
        for url in root.findall('url', ns):
            loc = url.find('loc', ns)
            if loc is not None and loc.text:
                existing_urls.add(loc.text.strip())
        
        # Получаем текущую дату в формате ISO
        current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        
        # Проверяем все статьи в папке blog
        new_articles_count = 0
        
        for filename in sorted(os.listdir(BLOG_DIR)):
            if filename.endswith(".html") and not filename.startswith("ПРИМЕР"):
                article_url = f"{SITE_URL}/blog/{filename}"
                
                # Если URL еще нет в sitemap, добавляем
                if article_url not in existing_urls:
                    # Создаем новый элемент url
                    url_elem = ET.SubElement(root, 'url')
                    
                    loc_elem = ET.SubElement(url_elem, 'loc')
                    loc_elem.text = f" {article_url}"  # Добавляем пробел в начале как в примере
                    
                    lastmod_elem = ET.SubElement(url_elem, 'lastmod')
                    lastmod_elem.text = current_date
                    
                    priority_elem = ET.SubElement(url_elem, 'priority')
                    priority_elem.text = '0.80'
                    
                    new_articles_count += 1
                    print(f"➕ Добавлена новая статья в sitemap: {filename}")
        
        if new_articles_count > 0:
            # Форматируем XML с отступами
            indent_xml(root)
            
            # Сохраняем обновленный sitemap
            tree.write(SITEMAP_FILE, encoding='UTF-8', xml_declaration=True)
            print(f"✅ Sitemap обновлен! Добавлено новых URL: {new_articles_count}")
        else:
            print("ℹ️ Новых статей для добавления в sitemap не найдено")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Файл {SITEMAP_FILE} не найден")
        return False
    except Exception as e:
        print(f"❌ Ошибка при обновлении sitemap: {e}")
        return False

def indent_xml(elem, level=0):
    """Добавляет отступы для красивого форматирования XML"""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent_xml(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

if __name__ == "__main__":
    print("="*50)
    print("🚀 Запуск синхронизатора блога")
    print("="*50)
    
    # Этап 1: Синхронизация секций blog-list
    print("\n📋 Этап 1: Поиск уникальной секции <section id='blog-list'>...")
    new_accordion_html = find_unique_section()
    
    if new_accordion_html:
        print("🔄 Обновляю все статьи новой секцией blog-list...")
        updated = update_all_articles(new_accordion_html)
        print(f"✅ Обновлено {updated} файлов!")
    
    # Этап 2: Обновление слайдера на главной странице
    print("\n📋 Этап 2: Обновление слайдера блога в index.html...")
    if update_index_blog_section():
        print("🎉 Главная страница успешно обновлена!")
    
    # Этап 3: Обновление sitemap.xml
    print("\n📋 Этап 3: Обновление sitemap.xml...")
    if update_sitemap():
        print("🗺️ Карта сайта успешно обновлена!")
    
    print("\n✨ Синхронизация завершена!")