# clean_and_seed.py
import os
import sys
from decimal import Decimal
import random
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from oscar.apps.catalogue.models import Product, ProductClass, Category
from oscar.apps.partner.models import Partner, StockRecord

def clean_and_seed():
    """Очистить старые товары и создать 50 новых"""
    
    print("🧹 Очистка старых товаров...")
    
    # Удаляем старые товары
    deleted_count, _ = Product.objects.all().delete()
    print(f"✅ Удалено товаров: {deleted_count}")
    
    # Также удалим старые stock records для чистоты
    StockRecord.objects.all().delete()
    
    print("\n🌱 Создание структуры магазина...")
    
    # Получаем или создаем ProductClass
    try:
        digital_class = ProductClass.objects.get(slug='digital')
        print("✅ Найден существующий класс продуктов 'digital'")
    except ProductClass.DoesNotExist:
        # Создаем новый ProductClass для цифровых товаров
        digital_class = ProductClass.objects.create(
            name="Digital Products",
            slug="digital",
            requires_shipping=False,
            track_stock=False,
        )
        print("✅ Создан новый класс продуктов 'digital'")
    
    # Получаем или создаем партнера
    try:
        partner = Partner.objects.get(code='digitalstore')
        print("✅ Найден существующий партнер 'digitalstore'")
    except Partner.DoesNotExist:
        # Создаем партнера если его нет
        partner = Partner.objects.create(
            name="Digital Store",
            code="digitalstore",
        )
        print("✅ Создан новый партнер 'digitalstore'")
    
    # Проверяем существование категорий и создаем их правильно
    categories_dict = {}
    categories_to_create = [
        ('software', 'Программное обеспечение'),
        ('ebooks', 'Электронные книги'),
        ('courses', 'Онлайн-курсы'),
        ('music', 'Музыка'),
        ('templates', 'Шаблоны'),
        ('assets', 'Ресурсы'),
    ]
    
    # Проверяем, существует ли уже главная категория
    try:
        root_category = Category.objects.get(depth=1)
        print("✅ Найдена корневая категория")
    except Category.DoesNotExist:
        # Создаем корневую категорию
        root_category = Category.add_root(
            name="Все товары",
            slug="all",
            description="Все категории товаров"
        )
        print("✅ Создана корневая категория 'Все товары'")
    
    # Создаем или получаем дочерние категории
    for slug, name in categories_to_create:
        try:
            cat = Category.objects.get(slug=slug)
            categories_dict[slug] = cat
            print(f"✅ Найдена существующая категория '{name}'")
        except Category.DoesNotExist:
            # Создаем категорию как дочернюю для корневой
            try:
                cat = root_category.add_child(
                    name=name,
                    slug=slug,
                    description=f"Категория {name}"
                )
                categories_dict[slug] = cat
                print(f"✅ Создана новая категория '{name}'")
            except Exception as e:
                # Если корневая категория недоступна, создаем как независимую
                print(f"⚠️ Не удалось создать как дочернюю, создаю как независимую категорию: {e}")
                cat = Category.add_root(
                    name=name,
                    slug=slug,
                    description=f"Категория {name}"
                )
                categories_dict[slug] = cat
                print(f"✅ Создана независимая категория '{name}'")
    
    # Получаем категории из словаря
    software_cat = categories_dict.get('software')
    ebooks_cat = categories_dict.get('ebooks')
    courses_cat = categories_dict.get('courses')
    music_cat = categories_dict.get('music')
    templates_cat = categories_dict.get('templates')
    assets_cat = categories_dict.get('assets')
    
    # Проверяем что все категории созданы
    if not all([software_cat, ebooks_cat, courses_cat, music_cat, templates_cat, assets_cat]):
        print("❌ Не удалось создать все категории!")
        return
    
    print("\n🌱 Создание новых товаров...")
    
    # Список товаров с описаниями
    products_data = [
        # Программное обеспечение (1-10)
        ("Office Suite Pro 2024", software_cat, Decimal("6990.00"), 
         "Полный офисный пакет для дома и бизнеса. Включает текстовый редактор, таблицы и презентации."),
        ("PhotoEditor AI", software_cat, Decimal("12990.00"), 
         "Редактор фотографий с искусственным интеллектом. Автоматическое улучшение и ретушь."),
        ("VideoStudio Ultimate", software_cat, Decimal("17990.00"), 
         "Профессиональный видеоредактор с эффектами и переходом."),
        ("Antivirus Security", software_cat, Decimal("3990.00"), 
         "Защита от вирусов и вредоносного ПО. Ежедневные обновления баз."),
        ("CodeEditor Pro", software_cat, Decimal("5990.00"), 
         "Продвинутый редактор кода для разработчиков. Поддержка всех языков."),
        ("3D Modeler", software_cat, Decimal("22990.00"), 
         "Программа для 3D моделирования и анимации."),
        ("AudioMaster Studio", software_cat, Decimal("14990.00"), 
         "Профессиональная студия звукозаписи и обработки."),
        ("Database Manager", software_cat, Decimal("8990.00"), 
         "Управление базами данных SQL и NoSQL."),
        ("Network Scanner", software_cat, Decimal("4990.00"), 
         "Анализ и мониторинг компьютерных сетей."),
        ("Backup System", software_cat, Decimal("2990.00"), 
         "Автоматическое резервное копирование данных."),
        
        # Электронные книги (11-20)
        ("Python Programming Guide", ebooks_cat, Decimal("1490.00"), 
         "Полное руководство по программированию на Python. От основ до продвинутых тем."),
        ("Web Development Handbook", ebooks_cat, Decimal("1990.00"), 
         "Современная веб-разработка: HTML, CSS, JavaScript, React."),
        ("Data Science Fundamentals", ebooks_cat, Decimal("1790.00"), 
         "Основы анализа данных и машинного обучения."),
        ("Business Strategy 2024", ebooks_cat, Decimal("2490.00"), 
         "Стратегии развития бизнеса в цифровую эпоху."),
        ("Digital Marketing Mastery", ebooks_cat, Decimal("1690.00"), 
         "Эффективный маркетинг в социальных сетях и интернете."),
        ("UI/UX Design Principles", ebooks_cat, Decimal("1890.00"), 
         "Принципы проектирования пользовательских интерфейсов."),
        ("Cybersecurity Basics", ebooks_cat, Decimal("1590.00"), 
         "Основы защиты информации и кибербезопасности."),
        ("Mobile App Development", ebooks_cat, Decimal("2090.00"), 
         "Разработка мобильных приложений для iOS и Android."),
        ("Cloud Computing Guide", ebooks_cat, Decimal("1790.00"), 
         "Работа с облачными технологиями AWS и Azure."),
        ("DevOps Practices", ebooks_cat, Decimal("1990.00"), 
         "Современные практики разработки и эксплуатации."),
        
        # Онлайн-курсы (21-30)
        ("Full Stack Web Developer", courses_cat, Decimal("49990.00"), 
         "Полный курс по веб-разработке. От HTML до React и Node.js."),
        ("Data Science Professional", courses_cat, Decimal("59990.00"), 
         "Профессиональный курс по анализу данных и машинному обучению."),
        ("UI/UX Design Bootcamp", courses_cat, Decimal("44990.00"), 
         "Интенсивный курс по дизайну пользовательских интерфейсов."),
        ("Digital Marketing Expert", courses_cat, Decimal("39990.00"), 
         "Комплексный курс по цифровому маркетингу."),
        ("Mobile Development Pro", courses_cat, Decimal("54990.00"), 
         "Разработка нативных и кросс-платформенных мобильных приложений."),
        ("Cybersecurity Specialist", courses_cat, Decimal("64990.00"), 
         "Подготовка специалистов по информационной безопасности."),
        ("Cloud Architecture", courses_cat, Decimal("52990.00"), 
         "Проектирование и развертывание облачных решений."),
        ("DevOps Engineering", courses_cat, Decimal("57990.00"), 
         "Курс по автоматизации процессов разработки и эксплуатации."),
        ("Game Development", courses_cat, Decimal("47990.00"), 
         "Создание игр на Unity и Unreal Engine."),
        ("AI & Machine Learning", courses_cat, Decimal("69990.00"), 
         "Продвинутый курс по искусственному интеллекту."),
        
        # Музыка (31-40)
        ("Electronic Vibes Collection", music_cat, Decimal("1490.00"), 
         "Коллекция электронных треков для видео и проектов."),
        ("Relaxation & Meditation", music_cat, Decimal("990.00"), 
         "Расслабляющая музыка для медитации и отдыха."),
        ("Cinematic Soundtracks", music_cat, Decimal("1990.00"), 
         "Эпические саундтреки для видео и презентаций."),
        ("Jazz Classics", music_cat, Decimal("1290.00"), 
         "Классические джазовые композиции в современной обработке."),
        ("Ambient Nature Sounds", music_cat, Decimal("790.00"), 
         "Звуки природы: лес, океан, дождь."),
        ("Rock Collection 2024", music_cat, Decimal("1690.00"), 
         "Сборник современных рок-композиций."),
        ("Sound Effects Library", music_cat, Decimal("2990.00"), 
         "Библиотека звуковых эффектов для видео и игр."),
        ("Classical Masterpieces", music_cat, Decimal("1390.00"), 
         "Шедевры классической музыки."),
        ("Lo-Fi Beats", music_cat, Decimal("1190.00"), 
         "Расслабляющие Lo-Fi композиции для работы и учебы."),
        ("World Music Collection", music_cat, Decimal("1590.00"), 
         "Музыка разных народов и культур."),
        
        # Шаблоны (41-45)
        ("Corporate Website Template", templates_cat, Decimal("7990.00"), 
         "Готовый шаблон корпоративного сайта на Bootstrap 5."),
        ("E-commerce Store Template", templates_cat, Decimal("11990.00"), 
         "Шаблон интернет-магазина с корзиной и каталогом."),
        ("Portfolio for Creatives", templates_cat, Decimal("4990.00"), 
         "Элегантный шаблон портфолио для дизайнеров и фотографов."),
        ("Landing Page Builder", templates_cat, Decimal("3990.00"), 
         "Конструктор лендингов с drag-and-drop интерфейсом."),
        ("Admin Dashboard Template", templates_cat, Decimal("8990.00"), 
         "Шаблон административной панели с графиками и таблицами."),
        
        # Ресурсы (46-50)
        ("UI Kit - Modern Design", assets_cat, Decimal("5990.00"), 
         "Комплект UI компонентов в современном стиле."),
        ("Icon Pack - 1000+ Icons", assets_cat, Decimal("2990.00"), 
         "Набор из более чем 1000 векторных иконок."),
        ("Font Collection - Pro", assets_cat, Decimal("4990.00"), 
         "Коллекция профессиональных шрифтов для коммерческого использования."),
        ("Texture Pack - 4K", assets_cat, Decimal("3990.00"), 
         "Набор текстур высокого разрешения для дизайна."),
        ("3D Models - Premium", assets_cat, Decimal("9990.00"), 
         "Коллекция 3D моделей для игр и визуализации."),
    ]
    
    # Создаем товары
    created_count = 0
    for i, (title, category, price, description) in enumerate(products_data, 1):
        try:
            # Генерируем уникальный UPC
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            upc = f"UPC{timestamp}{i:03d}"
            
            # Создаем продукт
            product = Product.objects.create(
                title=title,
                description=description,
                product_class=digital_class,
                structure=Product.STANDALONE,
                upc=upc,
                is_discountable=True,
            )
            
            # Добавляем категорию
            product.categories.add(category)
            
            # Stock record
            StockRecord.objects.create(
                product=product,
                partner=partner,
                partner_sku=f"SKU{timestamp}{i:03d}",
                price_currency='RUB',
                price=price,
                num_in_stock=random.randint(100, 1000),
                low_stock_threshold=10,
            )
            
            created_count += 1
            print(f"✅ Товар {i}: {title} - {price} RUB")
            
        except Exception as e:
            print(f"❌ Ошибка при создании товара {i}: {e}")
            continue
    
    print(f"\n🎉 Успешно создано {created_count} товаров!")
    print(f"📦 Класс продуктов: {digital_class.name}")
    print(f"🤝 Партнер: {partner.name}")
    print(f"📂 Категорий создано: {len(categories_dict)}")
    return created_count

if __name__ == '__main__':
    clean_and_seed()