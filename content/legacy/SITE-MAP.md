# Карта сайту diodi.if.ua

> Legacy-джерело: https://diodi.if.ua (Joomla 3, шаблон `t3_bs3_blank` / `eko-style`)  
> Екстракція: `content/legacy/` · скрипт: `scripts/extract_legacy_site.py`  
> Дата: 2026-07-01

---

## 1. Основна ідея та позиціонування

**Бренд:** стоматологічна клініка «ДіОДі» (ДіОДі / ДІОДІ)  
**Локація:** Івано-Франківськ  
**На ринку:** з 2001 року (24+ років)

### Місія

Надання повного спектра стоматологічних послуг «під одним дахом» — від діагностики та терапії до ортопедії, імплантології та власної зуботехнічної лабораторії.

### УТП (унікальні торгові пропозиції)

| # | УТП | Де на сайті |
|---|-----|-------------|
| 1 | Комплексне лікування без пошуку різних спеціалістів | Головна, Послуги |
| 2 | Інтраоральний цифровий 3D сканер | Головна, 3D сканування |
| 3 | Власна лабораторія Dio-Lab (CAD/CAM) | Лабораторія |
| 4 | Сучасне обладнання та сертифіковані матеріали | Про нас |
| 5 | Акцент на імплантологію | Головна (окремий блок) |
| 6 | Досвід команди з 2001 року | Головна, Про нас, Команда |

### Цільова аудиторія

Мешканці Івано-Франківська та області, які шукають надійну стоматологію з повним циклом послуг, сучасною діагностикою та можливістю запису онлайн / по телефону.

### Тон комунікації

Професійний, довірливий, з акцентом на досвід, комплексність та сучасні технології.

---

## 2. SEO-аудит legacy-сайту

### Поточний стан

| Параметр | Статус |
|----------|--------|
| `meta description` | Відсутній на всіх 31 сторінках |
| `meta keywords` | Відсутній |
| `og:title` / `og:description` | Відсутні |
| `og:image` | Лише на головній (thumbnail) |
| `<title>` | Коротка назва без бренду/міста |
| `robots.txt` | 404 |
| `sitemap.xml` | 404 |
| Мова | `uk-ua` |
| Canonical | Не задано |

### Рекомендації для нового сайту

Детальні `title`, `description`, `og:*` і `canonical` для кожної сторінки — у файлі [seo/recommendations.md](seo/recommendations.md).

**Приклад (головна):**

- **title:** `Стоматологія ДіОДі — клініка в Івано-Франківську`
- **description:** `Повний спектр стоматологічних послуг з 2001 року. Імплантація, терапія, ортопедія, 3D сканер. Запис: (050) 537-76-57.`
- **canonical:** `https://diodi.if.ua/`

### Соціальні сигнали (legacy)

- Twitter share text: «Вас вітає клініка сучасної стоматологіі «ДІОДІ»»
- Facebook Like / Twitter / Google+ кнопки на сторінках контенту

---

## 3. Карта сторінок

### 3.1. Дерево навігації

```
/ (Головна)
├── /pro-nas (Про нас)
│   ├── /pro-nas/nasha-komanda (Наша команда)
│   │   ├── /pro-nas/nasha-komanda/dyrektor
│   │   ├── /pro-nas/nasha-komanda/holovnyi-likar
│   │   ├── /pro-nas/nasha-komanda/likar-skovorodniev
│   │   ├── /pro-nas/nasha-komanda/administrator-platonova-olena
│   │   ├── /pro-nas/nasha-komanda/zubnyi-tekhnik-moderuk
│   │   ├── /pro-nas/nasha-komanda/molodshyi-medychnyi-personal-svintsytska-nataliia-valeriivna
│   │   ├── /pro-nas/nasha-komanda/cerednii-medychnyi-personal-petrushka-snizhana-serhiivna *
│   │   └── /pro-nas/nasha-komanda/cerednii-medychnyi-personal-volochii-ivanna-serhiivna
│   └── /pro-nas/fotohalereia (Фотогалерея)
├── /posluhy (Послуги)
│   ├── /posluhy/terapevtychna-stomatolohiia
│   │   ├── …/estetychna-restavratsiia
│   │   ├── …/endodontiia-likuvannia-korenevykh-kanaliv
│   │   ├── …/profesiina-hihiiena-rotovoi-porozhnyny
│   │   ├── …/plombuvannia-usikh-vydiv-kariiesu
│   │   ├── …/profesiine-vidbiliuvannia
│   │   └── …/likuvannia-paradontu
│   ├── /posluhy/ortopedychna-stomatolohiia
│   │   ├── …/neznimne-protezuvannia
│   │   └── …/znimne-protezuvannia
│   ├── /posluhy/khirurhiia
│   ├── /posluhy/implantolohiia
│   ├── /posluhy/renthenohrafiia
│   └── /posluhy/3d-skanuvannya
├── /labaratoriia (Лабораторія)
├── /tsiny (Ціни)
├── /vidhuky (Відгуки)
├── /kontakty (Контакти)
└── [external] https://dio-lazer.if.ua/ (Лазерна епіляція)
```

\* URL містить застарілий slug `petrushka-snizhana`, фактичний контент — Басараб Ірина Володимирівна.

### 3.2. Таблиця сторінок і файлів контенту

| URL | Title (legacy) | Файл контенту | Статус |
|-----|----------------|---------------|--------|
| `/` | Головна | [text/home.md](text/home.md) | ok |
| `/pro-nas` | Про нас | [text/pro-nas.md](text/pro-nas.md) | ok |
| `/pro-nas/nasha-komanda` | Наша команда | [text/team/nasha-komanda.md](text/team/nasha-komanda.md) | ok |
| `/pro-nas/fotohalereia` | Фотогалерея | [text/fotohalereia.md](text/fotohalereia.md) | ok |
| `/kontakty` | Контакти | [text/kontakty.md](text/kontakty.md) | ok |
| `/posluhy` | ПОСЛУГИ | [text/posluhy.md](text/posluhy.md) | ok |
| `/tsiny` | Ціни | [text/tsiny.md](text/tsiny.md) | ok |
| `/vidhuky` | Відгуки | [text/vidhuky.md](text/vidhuky.md) | ok |
| `/labaratoriia` | Лабораторія | [text/labaratoriia.md](text/labaratoriia.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia` | Терапевтична стоматологія | [text/posluhy/terapevtychna-stomatolohiia.md](text/posluhy/terapevtychna-stomatolohiia.md) | ok |
| `/posluhy/ortopedychna-stomatolohiia` | Ортопедична стоматологія | [text/posluhy/ortopedychna-stomatolohiia.md](text/posluhy/ortopedychna-stomatolohiia.md) | ok |
| `/posluhy/implantolohiia` | Імплантологія | [text/posluhy/implantolohiia.md](text/posluhy/implantolohiia.md) | ok |
| `/posluhy/renthenohrafiia` | Рентгенографія | [text/posluhy/renthenohrafiia.md](text/posluhy/renthenohrafiia.md) | ok |
| `/posluhy/khirurhiia` | Хірургія | [text/posluhy/khirurhiia.md](text/posluhy/khirurhiia.md) | ok |
| `/posluhy/3d-skanuvannya` | 3D сканування | [text/posluhy/3d-skanuvannya.md](text/posluhy/3d-skanuvannya.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia/endodontiia-…` | Ендодонтія | [text/posluhy/endodontiia.md](text/posluhy/endodontiia.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia/estetychna-restavratsiia` | Естетична реставрація | [text/posluhy/estetychna-restavratsiia.md](text/posluhy/estetychna-restavratsiia.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia/likuvannia-paradontu` | Лікування парадонту | [text/posluhy/likuvannia-paradontu.md](text/posluhy/likuvannia-paradontu.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia/plombuvannia-…` | Пломбування | [text/posluhy/plombuvannia.md](text/posluhy/plombuvannia.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia/profesiina-hihiiena-…` | Проф. гігієна | [text/posluhy/profesiina-hihiiena.md](text/posluhy/profesiina-hihiiena.md) | ok |
| `/posluhy/terapevtychna-stomatolohiia/profesiine-vidbiliuvannia` | Відбілювання | [text/posluhy/profesiine-vidbiliuvannia.md](text/posluhy/profesiine-vidbiliuvannia.md) | ok |
| `/posluhy/ortopedychna-stomatolohiia/neznimne-protezuvannia` | Незнімне протезування | [text/posluhy/neznimne-protezuvannia.md](text/posluhy/neznimne-protezuvannia.md) | ok |
| `/posluhy/ortopedychna-stomatolohiia/znimne-protezuvannia` | Знімне протезування | [text/posluhy/znimne-protezuvannia.md](text/posluhy/znimne-protezuvannia.md) | ok |
| `/pro-nas/nasha-komanda/dyrektor` | Джус Олег Дмитрович | [text/team/dyrektor.md](text/team/dyrektor.md) | ok |
| `/pro-nas/nasha-komanda/holovnyi-likar` | Лабій Надія Анатоліївна | [text/team/holovnyi-likar.md](text/team/holovnyi-likar.md) | ok |
| `/pro-nas/nasha-komanda/likar-skovorodniev` | Сковороднєв А.В. | [text/team/likar-skovorodniev.md](text/team/likar-skovorodniev.md) | ok |
| `/pro-nas/nasha-komanda/administrator-platonova-olena` | Джус Олена Семенівна | [text/team/administrator.md](text/team/administrator.md) | ok |
| `/pro-nas/nasha-komanda/…-petrushka-snizhana-…` | Басараб І.В. | [text/team/basarab.md](text/team/basarab.md) | ok |
| `/pro-nas/nasha-komanda/…-volochii-…` | Волочій І.С. | [text/team/volochii.md](text/team/volochii.md) | ok |
| `/pro-nas/nasha-komanda/…-svintsytska-…` | Свінціцка Н.В. | [text/team/svintsytska.md](text/team/svintsytska.md) | ok |
| `/pro-nas/nasha-komanda/zubnyi-tekhnik-moderuk` | Мадерук Ю.В. | [text/team/moderuk.md](text/team/moderuk.md) | ok |
| `/pro-nas/nasha-komanda/likar-stomatoloh-dubishchak-…` | Дубіщак В.Я. | — | **404** |
| `/pro-nas/nasha-komanda/…-dutchak-…` | Дутчак Г.М. | — | **404** |

Маніфест усіх сторінок: [text/index.json](text/index.json)

---

## 4. Інформаційні блоки

### 4.1. Глобальні (присутні на всіх сторінках)

| ID | Блок | Тип | Зміст |
|----|------|-----|-------|
| G01 | Header | навігація | Логотип `images/logo.jpg`, мегаменю |
| G02 | Footer — телефони | контакт | (050) 537-76-57, (067) 343-60-10 |
| G03 | Footer — email | контакт | diodi2001@gmail.com |
| G04 | Footer — «Про нас» | посилання | Про клініку, Команда, Контакти, Фотогалерея |
| G05 | Footer — «Наші послуги» | посилання | Терапія, Ортопедія, Імплантологія, Рентген |
| G06 | Footer — соцмережі | посилання | Instagram, Facebook |
| G07 | Форма «Замовити дзвінок» | форма | Ім'я*, телефон*, текст*, reCAPTCHA |
| G08 | Форма «Написати нам» | форма | Ім'я*, email*, текст*, reCAPTCHA |
| G09 | Copyright | текст | © www.diodi.if.ua · sd-studio.com.ua |
| G10 | Scroll to top | UI | Кнопка прокрутки вгору |

### 4.2. Головна `/`

| ID | Блок | Тип | Зміст |
|----|------|-----|-------|
| H01 | Hero | H1 | «Вас вітає клініка сучасної стоматологіі «ДІОДІ»» |
| H02 | Intro | текст | 24+ роки, з 2001, повний спектр послуг, комплексна система лікування |
| H03 | Чому обирають нас | H2 + текст | Комплекс послуг, 3D сканер, відновлення зубів |
| H04 | Галерея клініки | зображення | IMG_5507–5509, glavnaya/g-02–05 |
| H05 | Імплантація CTA | текст | «Імплантація — правильний вибір» |
| H06 | Імплантація опис | текст | Титановий імплантат, абатмент, коронки/протези |
| H07 | Імплантація image | зображення | poslugi/implantaciya.jpg |
| H08 | Соцкнопки | share | FB, Twitter, Google+ |

### 4.3. Про нас `/pro-nas`

| ID | Блок | Тип |
|----|------|-----|
| A01 | H1 «Про нашу клініку» | заголовок |
| A02 | Опис клініки | 4 абзаци про комплекс, індивідуальний підхід, обладнання |
| A03 | Зображення | про_нас.png |

### 4.4. Команда `/pro-nas/nasha-komanda`

| ID | Блок | Тип |
|----|------|-----|
| T01 | Сітка карток | 9 співробітників з фото, ПІБ, посада |
| T02 | CTA запис | телефони для запису |
| T03 | Профілі (окремі сторінки) | біографія + фото кожного |

**Склад команди (з live):**

1. Джус Олена Семенівна — адміністратор
2. Джус Олег Дмитрович — директор, провідний зубний технік
3. Лабій Надія Анатоліївна — головний лікар
4. Мадерук Юрій Васильович — зубний технік
5. Сковороднєв Андрій Васильович — лікар-стоматолог
6. Дубіщак Віталія Яківна — лікар-стоматолог (профіль 404)
7. Дутчак Галина Миколаівна — середній медперсонал (профіль 404)
8. Свінціцка Наталія Валеріівна — середній медперсонал
9. Басараб Ірина Володимирівна — середній медперсонал
10. Волочій Іванна Степанівна — середній медперсонал

### 4.5. Послуги `/posluhy` та підсторінки

| ID | Блок | Сторінки |
|----|------|----------|
| S01 | Вступ про комплексність | /posluhy |
| S02 | Список напрямів | /posluhy |
| S03 | Опис напряму + зображення | кожна підсторінка |
| S04 | Підпослуги терапії | 6 сторінок |
| S05 | Підпослуги ортопедії | 2 сторінки |
| S06 | Хірургія, імплантологія, рентген, 3D | окремі сторінки |

### 4.6. Ціни `/tsiny`

| ID | Блок | Тип |
|----|------|-----|
| P01 | H1 «Ціни» | заголовок |
| P02 | Прейскурант | таблиця (~40 позицій): терапія, канали, ортопедія, хірургія |
| P03 | Підпис | «Затверджено Директор п/п «ДіОДі» О.Д. Джус» |

### 4.7. Контакти `/kontakty`

| ID | Блок | Зміст |
|----|------|-------|
| C01 | Телефони | +38 (050) 537-76-57, +38 (067) 343-60-10 |
| C02 | Email | diodi2001@gmail.com |
| C03 | Графік | Пн–Пт 9:30–21:00, Сб за записом, Нд вихідний |
| C04 | Карта | Google Maps embed (~48.905, 24.681) |

### 4.8. Фотогалерея `/pro-nas/fotohalereia`

| ID | Блок | Зміст |
|----|------|-------|
| F01 | Галерея | ~20 фото в `images/fotogalereya/` |

### 4.9. Лабораторія `/labaratoriia`

| ID | Блок | Зміст |
|----|------|-------|
| L01 | Dio-Lab | Зуботехнічна лабораторія, CAD/CAM, повний цикл |

### 4.10. Відгуки `/vidhuky`

| ID | Блок | Зміст |
|----|------|-------|
| R01 | JComments | Динамічні відгуки (контент не екстраговано) |

---

## 5. Контакти та зовнішні ресурси

### Контакти

- **Телефони:** +38 (050) 537-76-57 · +38 (067) 343-60-10
- **Email:** diodi2001@gmail.com
- **Графік:** Пн–Пт 9:30–21:00 · Сб за записом · Нд вихідний
- **Координати:** 48.9051853, 24.6809897

### Соцмережі

- Instagram: https://www.instagram.com/clinicdiodi
- Facebook: https://www.facebook.com/profile.php?id=100063695671216

### Зовнішні ресурси

| Ресурс | URL | Примітка |
|--------|-----|----------|
| Лазерна епіляція | https://dio-lazer.if.ua/ | Окремий сайт, посилання в меню |
| Розробник legacy | sd-studio.com.ua | Copyright у футері |

---

## 6. Медіа-активи

### Зображення

- **Папка:** [images/](images/)
- **Кількість:** 60 унікальних оригіналів (без thumbnails)
- **Логотип:** `images/logo.jpg`

### Текстовий контент

- **Папка:** [text/](text/)
- **Формат:** Markdown з frontmatter (`source_url`, `title`, `slug`)
- **Маніфест:** [text/index.json](text/index.json)

---

## 7. Кольорова палітра

Лише кольори бренду для майбутнього редизайну — без typography і layout.

**Файл:** [styles/palette.css](styles/palette.css)

| Токен | HEX | Призначення |
|-------|-----|-------------|
| `--color-primary` | `#006ec7` | Основний синій (кнопки, акценти) |
| `--color-primary-hover` | `#0088cc` | Hover |
| `--color-primary-dark` | `#0359a2` | Темніший синій |
| `--color-accent` | `#d3dd40` | Лаймовий акцент |
| `--color-accent-alt` | `#8eae0b` | Оливковий акцент |
| `--color-blue-light` | `#37b5d3` | Світло-блакитний |
| `--color-bg-cream` | `#f3f3d5` | Кремовий фон |
| `--color-bg-mint` | `#f5fae2` | М'ятний фон |
| `--color-text` | `#333333` | Основний текст |

---

## 8. Зв'язок із Django-проєктом

Моделі в `src/pages/models.py` (`MainPage`, `InfoBlock`, `Gallery`, `GeneralSettings`) частково відповідають структурі legacy-сайту.

**Наступний крок (поза поточним scope):** імпорт `content/legacy/` у Django admin / fixtures після підтвердження карти.

---

## 9. Повторна екстракція

```bash
python3 scripts/extract_legacy_site.py
```

Скрипт ідемпотентний: перезаписує текст, доповнює зображення, оновлює `index.json` і `seo/recommendations.md`.
