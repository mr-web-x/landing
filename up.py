import os
from bs4 import BeautifulSoup
from collections import defaultdict
import re

BLOG_DIR = "blog"
INDEX_FILE = "index.html"
ACCORDION_ID = "blog-list"
BLOG_SECTION_ID = "blog"

def extract_section_content(html_content, section_id):
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
    
    print("\n✨ Синхронизация завершена!")