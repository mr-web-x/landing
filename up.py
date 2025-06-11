import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re
from datetime import datetime
import xml.etree.ElementTree as ET

BLOG_DIR = "blog"
TYPY_POZICIEK_DIR = "typy-poziciek"  # Новая папка
INDEX_FILE = "index.html"
BLOG_PAGE_FILE = "blog.html"
TYPY_POZICIEK_PAGE_FILE = "typy-poziciek.html"  # Новая страница
ACCORDION_ID = "blog-list"
BLOG_SECTION_ID = "blog"
BLOG_PAGE_SECTION_CLASS = "blog-content"
SITEMAP_FILE = "sitemap.xml"
SITE_URL = "https://fastcredit.sk"

def extract_section_content(html_content, section_id):
    """Извлекает содержимое секции по её ID"""
    soup = BeautifulSoup(html_content, "html.parser")
    section = soup.find("section", {"id": section_id})
    return str(section).strip() if section else ""

def extract_article_info(filepath, folder_name):
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
            "href": f"/{folder_name}/{filename}"
        }

def generate_blog_slider_html(articles):
    """Генерирует HTML для слайдера блога на главной странице"""
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

def generate_blog_page_html(articles):
    """Генерирует HTML для страницы блога"""
    cards_html = ""
    
    for article in articles:
        card = f'''            <a
              class="blog-content__card"
              href="{article['href']}"
            >
              <img alt="articles" loading="lazy" src="/assets/blog/b1.webp" />
              <h3>
                {article['title']}
              </h3>
              <p>
                {article['description']}
              </p>
              <div class="blog-card-bottom">
                <span>Podrobnosti →</span>
              </div>
            </a>
'''
        cards_html += card
    
    # Создаем полную секцию для страницы блога
    section_html = f'''      <section class="blog-content">
        <div class="container">
          <h1>Náš blog</h1>
          <div class="blog-content__list">
{cards_html.rstrip()}
          </div>
        </div>
      </section>'''
    
    return section_html

def generate_typy_poziciek_page_html(articles):
    """Генерирует HTML для страницы typy-poziciek"""
    cards_html = ""
    
    for article in articles:
        card = f'''            <a
              class="blog-content__card"
              href="{article['href']}"
            >
              <img alt="articles" loading="lazy" src="/assets/blog/b1.webp" />
              <h3>
                {article['title']}
              </h3>
              <p>
                {article['description']}
              </p>
              <div class="blog-card-bottom">
                <span>Podrobnosti →</span>
              </div>
            </a>
'''
        cards_html += card
    
    # Создаем полную секцию для страницы typy-poziciek
    section_html = f'''      <section class="blog-content">
        <div class="container">
          <h1>Typy pôžičiek</h1>
          <div class="blog-content__list">
{cards_html.rstrip()}
          </div>
        </div>
      </section>'''
    
    return section_html

def find_unique_section():
    """Находит уникальную секцию blog-list среди всех файлов блога"""
    content_map = defaultdict(list)
    
    # Сканируем только папку blog для поиска уникальной секции
    if not os.path.exists(BLOG_DIR):
        print(f"⚠️ Папка {BLOG_DIR} не существует")
        return None
    
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".html"):
            path = os.path.join(BLOG_DIR, filename)
            with open(path, "r", encoding="utf-8") as file:
                html = file.read()
                section_html = extract_section_content(html, ACCORDION_ID)
                if section_html:
                    content_map[section_html].append(filename)

    if len(content_map) == 0:
        print("⚠️ Не найдено секций blog-list в папке blog")
        return None

    if len(content_map) == 1:
        print("⚠️ Все секции blog-list одинаковые — нечего обновлять.")
        return None

    for content, files in content_map.items():
        if len(files) == 1:
            print(f"✅ Найдена уникальная секция blog-list в файле: {files[0]}")
            return content

    print("❌ Нет уникальной секции blog-list — либо все разные, либо повторяются по нескольку раз.")
    return None

def update_articles_in_folder(folder_path, folder_name, new_section_html):
    """Обновляет секцию blog-list во всех файлах указанной папки"""
    if not os.path.exists(folder_path):
        print(f"⚠️ Папка {folder_path} не существует")
        return 0
    
    updated_count = 0
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            path = os.path.join(folder_path, filename)
            with open(path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            old_section = soup.find("section", {"id": ACCORDION_ID})
            if old_section:
                new_section_soup = BeautifulSoup(new_section_html, "html.parser")
                old_section.replace_with(new_section_soup)
                
                with open(path, "w", encoding="utf-8") as file:
                    file.write(str(soup))
                updated_count += 1
                print(f"  ✓ Обновлен файл: {folder_name}/{filename}")
    
    return updated_count

def sync_blog_list_sections():
    """Синхронизирует секции blog-list между всеми файлами в обеих папках"""
    print("\n📋 Этап 5: Синхронизация секций <section id='blog-list'>...")
    
    # Ищем уникальную секцию только в папке blog
    new_section_html = find_unique_section()
    
    if not new_section_html:
        return False
    
    total_updated = 0
    
    # Обновляем все файлы в папке blog
    print("🔄 Обновляю файлы в папке blog...")
    blog_updated = update_articles_in_folder(BLOG_DIR, "blog", new_section_html)
    total_updated += blog_updated
    
    # Обновляем все файлы в папке typy-poziciek
    print("🔄 Обновляю файлы в папке typy-poziciek...")
    typy_updated = update_articles_in_folder(TYPY_POZICIEK_DIR, "typy-poziciek", new_section_html)
    total_updated += typy_updated
    
    if total_updated > 0:
        print(f"✅ Синхронизация завершена! Обновлено файлов:")
        print(f"   - blog: {blog_updated}")
        print(f"   - typy-poziciek: {typy_updated}")
        print(f"   - Всего: {total_updated}")
        return True
    else:
        print("⚠️ Ни один файл не был обновлен")
        return False

def get_articles_from_folder(folder_path, folder_name):
    """Получает список статей из указанной папки"""
    articles = []
    
    if not os.path.exists(folder_path):
        print(f"⚠️ Папка {folder_path} не существует")
        return articles
    
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".html"):
            path = os.path.join(folder_path, filename)
            article_info = extract_article_info(path, folder_name)
            if article_info:  # None если файл начинается с "ПРИМЕР"
                articles.append(article_info)
    
    return articles

def update_index_blog_section():
    """Обновляет секцию блога в index.html на основе всех статей из папки blog"""
    articles = get_articles_from_folder(BLOG_DIR, "blog")
    
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

def update_blog_page_section():
    """Обновляет секцию блога в blog.html на основе статей из папки blog"""
    articles = get_articles_from_folder(BLOG_DIR, "blog")
    
    if not articles:
        print("❌ Не найдено статей для обновления в blog.html")
        return False
    
    # Генерируем новый HTML для страницы блога
    new_blog_section = generate_blog_page_html(articles)
    
    # Обновляем blog.html
    try:
        with open(BLOG_PAGE_FILE, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
        
        old_section = soup.find("section", {"class": BLOG_PAGE_SECTION_CLASS})
        if old_section:
            new_section_soup = BeautifulSoup(new_blog_section, "html.parser")
            new_section_soup = new_section_soup.find("section")  # Извлекаем только секцию
            old_section.replace_with(new_section_soup)
            
            with open(BLOG_PAGE_FILE, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"✅ Обновлена страница блога в blog.html ({len(articles)} статей)")
            return True
        else:
            print("❌ Не найдена секция блога в blog.html")
            return False
            
    except FileNotFoundError:
        print(f"❌ Файл {BLOG_PAGE_FILE} не найден")
        return False
    except Exception as e:
        print(f"❌ Ошибка при обновлении blog.html: {e}")
        return False

def update_typy_poziciek_page_section():
    """Обновляет секцию в typy-poziciek.html на основе статей из папки typy-poziciek"""
    articles = get_articles_from_folder(TYPY_POZICIEK_DIR, "typy-poziciek")
    
    if not articles:
        print("❌ Не найдено статей для обновления в typy-poziciek.html")
        return False
    
    # Генерируем новый HTML для страницы typy-poziciek
    new_section = generate_typy_poziciek_page_html(articles)
    
    # Обновляем typy-poziciek.html
    try:
        with open(TYPY_POZICIEK_PAGE_FILE, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
        
        old_section = soup.find("section", {"class": BLOG_PAGE_SECTION_CLASS})
        if old_section:
            new_section_soup = BeautifulSoup(new_section, "html.parser")
            new_section_soup = new_section_soup.find("section")  # Извлекаем только секцию
            old_section.replace_with(new_section_soup)
            
            with open(TYPY_POZICIEK_PAGE_FILE, "w", encoding="utf-8") as file:
                file.write(str(soup))
            
            print(f"✅ Обновлена страница typy-poziciek в typy-poziciek.html ({len(articles)} статей)")
            return True
        else:
            print("❌ Не найдена секция в typy-poziciek.html")
            return False
            
    except FileNotFoundError:
        print(f"❌ Файл {TYPY_POZICIEK_PAGE_FILE} не найден")
        return False
    except Exception as e:
        print(f"❌ Ошибка при обновлении typy-poziciek.html: {e}")
        return False

def update_sitemap():
    """Обновляет sitemap.xml, добавляя новые статьи из обеих папок"""
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
        
        new_articles_count = 0
        
        # Проверяем статьи из папки blog
        if os.path.exists(BLOG_DIR):
            for filename in sorted(os.listdir(BLOG_DIR)):
                if filename.endswith(".html") and not filename.startswith("ПРИМЕР"):
                    article_url = f"{SITE_URL}/blog/{filename}"
                    
                    if article_url not in existing_urls:
                        url_elem = ET.SubElement(root, 'url')
                        
                        loc_elem = ET.SubElement(url_elem, 'loc')
                        loc_elem.text = f" {article_url}"
                        
                        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
                        lastmod_elem.text = current_date
                        
                        priority_elem = ET.SubElement(url_elem, 'priority')
                        priority_elem.text = '0.80'
                        
                        new_articles_count += 1
                        print(f"➕ Добавлена новая статья в sitemap: blog/{filename}")
        
        # Проверяем статьи из папки typy-poziciek
        if os.path.exists(TYPY_POZICIEK_DIR):
            for filename in sorted(os.listdir(TYPY_POZICIEK_DIR)):
                if filename.endswith(".html") and not filename.startswith("ПРИМЕР"):
                    article_url = f"{SITE_URL}/typy-poziciek/{filename}"
                    
                    if article_url not in existing_urls:
                        url_elem = ET.SubElement(root, 'url')
                        
                        loc_elem = ET.SubElement(url_elem, 'loc')
                        loc_elem.text = f" {article_url}"
                        
                        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
                        lastmod_elem.text = current_date
                        
                        priority_elem = ET.SubElement(url_elem, 'priority')
                        priority_elem.text = '0.80'
                        
                        new_articles_count += 1
                        print(f"➕ Добавлена новая статья в sitemap: typy-poziciek/{filename}")
        
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
    
    # Этап 1: Обновление слайдера на главной странице
    print("\n📋 Этап 1: Обновление слайдера блога в index.html...")
    if update_index_blog_section():
        print("🎉 Главная страница успешно обновлена!")
    
    # Этап 2: Обновление страницы блога
    print("\n📋 Этап 2: Обновление страницы блога в blog.html...")
    if update_blog_page_section():
        print("🎉 Страница блога успешно обновлена!")
    
    # Этап 3: Обновление страницы typy-poziciek
    print("\n📋 Этап 3: Обновление страницы typy-poziciek в typy-poziciek.html...")
    if update_typy_poziciek_page_section():
        print("🎉 Страница typy-poziciek успешно обновлена!")
    
    # Этап 4: Обновление sitemap.xml
    print("\n📋 Этап 4: Обновление sitemap.xml...")
    if update_sitemap():
        print("🗺️ Карта сайта успешно обновлена!")
    
    # Этап 5: Синхронизация секций blog-list
    if sync_blog_list_sections():
        print("🔗 Секции blog-list успешно синхронизированы!")
    
    print("\n✨ Синхронизация завершена!")