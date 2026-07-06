# PROMPT: Redesign сайту стоматології «ДіОДі» — diodi.if.ua

> Джерела: [content/legacy/SITE-MAP.md](../content/legacy/SITE-MAP.md), [docs/DATABASE-SCHEMA.md](DATABASE-SCHEMA.md), [content/legacy/styles/palette.css](../content/legacy/styles/palette.css)  
> Для cloud design tools: Open Design, Figma AI, аналоги.

---

## Роль і мета

Ти — senior product + brand designer. Створи **повний UI/UX redesign** сайту стоматологічної клініки **«ДіОДі»** (Івано-Франківськ, Україна). Це **не SPA** — дизайн під **server-rendered сайт** (Django + HTMX + vanilla JS + plain CSS). Потрібен сучасний, чистий, медично-надійний вигляд з акцентом на довіру, досвід (24+ років) і технології (3D сканер, власна лабораторія).

**Мова інтерфейсу:** українська (`uk-UA`).  
**Цільова аудиторія:** мешканці Івано-Франківська та області, 25–65+, сім'ї, люди, що шукають комплексну стоматологію «під одним дахом».

---

## Бренд і позиціонування

**Назва:** Стоматологія «ДіОДі» / «ДІОДІ»  
**Місто:** Івано-Франківськ  
**На ринку:** з 2001 року  

**Місія:** повний спектр стоматологічних послуг в одній клініці — від діагностики до імплантології та власної зуботехнічної лабораторії Dio-Lab.

**УТП (обов'язково відобразити в UI):**

1. Комплексне лікування — усі спеціалісти в одній клініці  
2. Інтраоральний цифровий 3D сканер  
3. Власна лабораторія Dio-Lab (CAD/CAM)  
4. Сучасне обладнання, сертифіковані матеріали  
5. Сильний акцент на **імплантологію** (окремий промо-блок на головній)  
6. Досвід команди 24+ років  

**Тон:** професійний, спокійний, довірливий. Без агресивного маркетингу. Акцент на турботу, безпеку, технологічність.

---

## Кольорова палітра (строго дотримуватись)

Використовуй **лише ці токени** (legacy бренд, оновлений layout):

| Token | HEX | Використання |
|-------|-----|--------------|
| Primary | `#006ec7` | CTA, посилання, активні стани |
| Primary hover | `#0088cc` | hover кнопок |
| Primary dark | `#0359a2` | header/footer акценти |
| Primary darker | `#003e71` | deep accents |
| Accent lime | `#d3dd40` | badges, highlights, secondary CTA |
| Accent alt | `#8eae0b` | icons, labels |
| Accent bright | `#e9f35c` | subtle highlights |
| Blue light | `#37b5d3` | info blocks, icons |
| Blue mid | `#5796c8` | secondary links |
| BG cream | `#f3f3d5` | alternate sections |
| BG mint | `#f5fae2` | soft sections |
| BG white | `#fafdfe` | main background |
| BG gray | `#f3f3f3` | cards, tables |
| Text | `#333333` | body |
| Text dark | `#1a1a1a` | headings |
| Text muted | `#777777` | captions |
| Border | `#dddddd` | dividers |
| White | `#ffffff` | cards, header |

**Заборонено:** inline styles, `!important`, random gradients поза палітрою, «медичний» cliché (надмірно червоний хрест, stock-smile overload).

---

## Типографіка (запропонуй у design system)

- **Headings:** сучасний sans-serif з характером (напр. Manrope, Plus Jakarta Sans або аналог) — чіткі, не агресивні  
- **Body:** system-friendly sans (Inter / Source Sans 3) — good Ukrainian Cyrillic  
- **Scale:** H1 40–48 desktop / 28–32 mobile; H2 32/24; H3 24/20; body 16–18; small 14  
- **Line-height:** 1.5–1.65 для body; headings 1.15–1.25  
- **Max line length:** 65–75ch для текстових блоків  

---

## Design system — компоненти

Створи reusable components:

### Global

- **Header (sticky):** logo left, mega-menu center, phone CTA right `(050) 537-76-57`  
- **Mobile header:** hamburger, logo, click-to-call icon  
- **Mega-menu «Послуги»:** 2 рівні (категорія → підпослуги)  
- **Footer (4 колонки):** контакти | Про нас | Послуги (4 featured) | соцмережі  
- **Primary button:** синій `#006ec7`, pill або rounded 8px  
- **Secondary button:** outline primary або accent lime  
- **Phone CTA button:** prominent, `tel:` link  
- **Form inputs:** name, phone, email, textarea — з labels і error states  
- **reCAPTCHA placeholder** (не малюй ключі)  
- **Breadcrumbs** для вкладених сторінок  
- **Section wrapper:** max-width ~1200px, padding responsive  
- **Card:** service / team / review — shadow subtle, radius 12px  
- **Price table:** category headers + rows (назва | ціна)  
- **Gallery grid:** masonry або uniform grid, lightbox trigger  
- **Map embed block:** 16:9 responsive  
- **Scroll-to-top** FAB (optional)  

### States

- hover, focus-visible (accessibility), disabled, loading для форм  
- empty states для відгуків  

---

## Responsive (обов'язково)

Design **3 breakpoints minimum:**

- **Desktop** 1440 / 1280  
- **Tablet** 768  
- **Mobile** 375 (iPhone) + **safe-area** для notch (`viewport-fit=cover`)  

**iOS Safari specifics:**

- sticky header не ламає scroll  
- click-to-call без auto-styling номерів  
- форми: font-size ≥16px (anti-zoom)  
- touch targets ≥44px  

---

## Карта сторінок (information architecture)

```
/                           Головна
/pro-nas                    Про клініку
/pro-nas/nasha-komanda      Команда (сітка)
/pro-nas/nasha-komanda/{slug}  Профіль лікаря
/pro-nas/fotohalereia       Фотогалерея
/posluhy                    Послуги (index)
/posluhy/{slug}             Категорія послуги
/posluhy/{parent}/{slug}    Підпослуга
/labaratoriia               Лабораторія Dio-Lab
/tsiny                      Ціни (прейскурант)
/vidhuky                    Відгуки
/kontakty                   Контакти
[external] dio-lazer.if.ua  Лазерна епіляція (нове вікно)
```

---

## Мапінг UI → моделі БД

| UI-розділ | Django-модель |
|-----------|---------------|
| Header, footer contacts | `SiteSettings`, `SocialLink` |
| Головна | `HomePage`, `HomeGalleryImage` |
| Про клініку | `AboutPage` |
| Команда / профілі | `TeamMember` |
| Послуги | `ServicesIndexPage`, `Service` (tree) |
| Лабораторія | `LaboratoryPage` |
| Ціни | `PriceList`, `PriceCategory`, `PriceItem` |
| Галерея | `Gallery`, `GalleryImage` |
| Відгуки | `Review` |
| Контакти | `ContactsPage` + `SiteSettings` |
| Форми | `ContactSubmission` |

---

## Сторінка 1: Головна `/`

**Модель даних:** `HomePage` + `HomeGalleryImage` + `SiteSettings`

### Секції зверху вниз

1. **Hero**
   - H1: «Вас вітає клініка сучасної стоматології «ДІОДІ»»
   - Підзаголовок: 24+ роки, Івано-Франківськ, з 2001
   - CTA: «Записатись» + «Подзвонити»
   - Фон: світлий, можливо фото клініки / abstract medical clean

2. **Intro block**
   - Текст про повний спектр послуг, комплексну систему лікування
   - 3–4 icon-benefits: діагностика, лікування, профілактика

3. **«Чому обирають нас?»**
   - H2 + текст про комплекс послуг без пошуку різних спеціалістів
   - Окремий highlight: **3D інтраоральний сканер**
   - Layout: text + image або 2-column

4. **Галерея клініки**
   - 8 фото (horizontal scroll mobile / grid desktop)
   - Lightbox interaction hint

5. **Імплантологія promo block** (важливий!)
   - CTA текст: «Імплантація — правильний вибір»
   - Пояснення: імплантат, абатмент, коронки/протези
   - Image right, text left (reverse on mobile)
   - CTA → `/posluhy/implantolohiia`

6. **Featured services grid**
   - 6 карток top-level послуг з іконкою/фото

7. **Team teaser**
   - 3–4 ключові лікарі → link «Вся команда»

8. **Dual contact strip** (перед footer)
   - Форма «Замовити дзвінок» | «Написати нам» (2 колонки desktop, stack mobile)

9. **Footer** (global)

---

## Сторінка 2: Про клініку `/pro-nas`

**Модель:** `AboutPage`

- Hero з H1 «Про нашу клініку»
- 4 абзаци: комплекс, індивідуальний підхід, обладнання, матеріали
- Image block (interior/clinic)
- CTA до команди та послуг

---

## Сторінка 3: Команда `/pro-nas/nasha-komanda`

**Модель:** `TeamMember` (ordered grid)

| Ім'я | Посада |
|------|--------|
| Джус Олена Семенівна | Адміністратор |
| Джус Олег Дмитрович | Директор, провідний зубний технік |
| Лабій Надія Анатоліївна | Головний лікар |
| Мадерук Юрій Васильович | Зубний технік |
| Сковороднєв Андрій Васильович | Лікар-стоматолог |
| Дубіщак Віталія Яківна | Лікар-стоматолог |
| Дутчак Галина Миколаівна | Середній медперсонал |
| Свінціцка Наталія Валеріівна | Середній медперсонал |
| Басараб Ірина Володимирівна | Середній медперсонал |
| Волочій Іванна Степанівна | Середній медперсонал |

**Card:** фото, short name, role, hover → «Детальніше»  
**Bottom CTA:** «Записатись» + телефони

---

## Сторінка 4: Профіль співробітника `/pro-nas/nasha-komanda/{slug}`

**Модель:** `TeamMember`

- Breadcrumbs  
- Layout: photo left (40%), bio right  
- H1 full name, role_title, bio paragraphs  
- Sidebar: «Записатись до лікаря» + phones  
- Optional: related services (M2M)

---

## Сторінка 5: Послуги index `/posluhy`

**Модель:** `ServicesIndexPage` + root `Service` items

- H1 «Послуги»
- Intro про комплексність
- Grid/list 6 категорій top-level:
  - Терапевтична стоматологія (+6 children indicator)
  - Ортопедична (+2)
  - Хірургія
  - Імплантологія
  - Рентгенографія
  - 3D сканування

---

## Сторінка 6: Категорія / підпослуга `/posluhy/...`

**Модель:** `Service` (parent/child)

- Breadcrumbs (Послуги → Терапевтична → Ендодонтія)
- H1 title, hero image optional
- Body text
- If parent: grid of child services
- If leaf: CTA «Записатись», related prices link
- Sidebar: phone, other services

**Дерево послуг:**

```
terapevtychna-stomatolohiia
  ├── estetychna-restavratsiia
  ├── endodontiia-likuvannia-korenevykh-kanaliv
  ├── profesiina-hihiiena-rotovoi-porozhnyny
  ├── plombuvannia-usikh-vydiv-kariiesu
  ├── profesiine-vidbiliuvannia
  └── likuvannia-paradontu
ortopedychna-stomatolohiia
  ├── neznimne-protezuvannia
  └── znimne-protezuvannia
khirurhiia | implantolohiia | renthenohrafiia | 3d-skanuvannya
```

---

## Сторінка 7: Лабораторія `/labaratoriia`

**Модель:** `LaboratoryPage`

- H1 «Dio-Lab» / Лабораторія
- Акцент: CAD/CAM, повний виробничий цикл
- Gallery equipment photos
- Trust block: зв'язок з клінікою

---

## Сторінка 8: Ціни `/tsiny`

**Модель:** `PriceList` → `PriceCategory` → `PriceItem`

- H1 «Ціни»
- Subtitle: «ПРЕЙСКУРАНТ (грн.)»
- **4 секції таблиць:**
  1. Терапевтичні роботи  
  2. Лікування каналів  
  3. Ортопедія  
  4. Хірургія  

- Row format: назва послуги | ціна (450.00 / «від 250.00»)
- Footer note: «Затверджено Директор п/п «ДіОДі» О.Д. Джус»
- Mobile: cards stack замість wide table
- Disclaimer: ціни можуть змінюватись

**Приклади позицій:** Консультація 450 грн, фотополімерна пломба 2450 грн, одноканальний зуб від 1500 грн

---

## Сторінка 9: Фотогалерея `/pro-nas/fotohalereia`

**Модель:** `Gallery` + ~20 `GalleryImage`

- Uniform or masonry grid
- Lightbox overlay
- Lazy-load placeholders

---

## Сторінка 10: Відгуки `/vidhuky`

**Модель:** `Review`

- List of review cards: author, text, optional stars
- Moderation state — показувати лише published
- Empty state: «Будьте першим, хто залишить відгук»
- NO legacy JComments UI

---

## Сторінка 11: Контакти `/kontakty`

**Модель:** `ContactsPage` + `SiteSettings`

- H1 «Контакти»
- Phones: +38 (050) 537-76-57, +38 (067) 343-60-10
- Email: diodi2001@gmail.com
- **Графік:**
  - Пн–Пт 9:30–21:00
  - Субота — за записом
  - Неділя — вихідний
- Google Maps embed (48.905185, 24.680990)
- Duplicate contact forms (callback + email)

---

## Global: Header navigation

**Top-level menu:**

- Головна
- Про нас ▾ (Про клініку, Команда, Фотогалерея)
- Послуги ▾ (mega-menu, 2 levels)
- Лабораторія
- Ціни
- Відгуки
- Контакти
- **External:** Лазерна епіляція → dio-lazer.if.ua (icon external link)

**Header right:** click-to-call primary phone

---

## Global: Footer

**Col 1 — Контакти:** phones, email  
**Col 2 — Про нас:** Про клініку, Команда, Контакти, Фотогалерея  
**Col 3 — Послуги (featured 4):** Терапія, Ортопедія, Імплантологія, Рентген  
**Col 4 — Соцмережі:** Instagram, Facebook  

**Copyright:** © Стоматологія ДіОДі, Івано-Франківськ

---

## Global: Форми (2 типи)

### «Замовити дзвінок»

- Ім'я* (text)
- Телефон* (tel)
- Текст* (textarea)
- reCAPTCHA
- Submit: «ВІДПРАВИТИ»
- Success: «Дякуємо! Ваше повідомлення відправлено…»

### «Написати нам»

- Ім'я*, Email*, Текст*
- reCAPTCHA
- Same success/error states

Design error states для кожного поля.

---

## Контент для placeholder-текстів (real copy)

**Hero H1:** «Вас вітає клініка сучасної стоматології «ДІОДІ»»

**Intro:** «Стоматологічна клініка «ДіОДі» в Івано-Франківську вже понад 24 роки успішно надає повний спектр стоматологічних послуг…»

**3D highlight:** «Команда лікарів і зубних техніків працює з ультрасучасним інтраоральним цифровим 3D сканером»

**Implant CTA:** «Увага! Вибір за Вами! Імплантація — це правильний вибір!»

**SEO title pattern:** `{Page Title} | Стоматологія ДіОДі, Івано-Франківськ`

---

## Deliverables (що згенерувати)

1. **Design system page:** colors, typography, buttons, forms, cards, spacing (4/8 grid)  
2. **Desktop + Mobile** для ключових екранів:
   - Головна (full scroll)
   - Послуги index
   - Сторінка послуги (leaf)
   - Команда + профіль
   - Ціни
   - Контакти
3. **Components sheet:** header, footer, mega-menu, forms, price table, gallery, review card  
4. **Prototype links** між основними flow: Home → Service → Contact, Home → Team → Profile  
5. **Annotations:** spacing, font sizes, component names (BEM-friendly: `header`, `hero`, `service-card`, `price-table`, `contact-form`)

---

## Технічні обмеження для handoff

- NO React/Vue/SPA layout assumptions  
- NO inline styles in final HTML  
- NO `!important` in CSS  
- Icons: SVG sprite or inline SVG  
- Images: placeholder ratio 16:9 hero, 1:1 team, 4:3 gallery  
- Forms будуть HTMX/ajax — design submit loading state  
- Mega-menu: CSS + vanilla JS, not heavy animation  

---

## Anti-patterns (уникати)

- Generic «dentist template» з надмірно білим sterile look без брендових кольорів  
- Stock photos з unnaturally white teeth everywhere  
- Cluttered legacy Joomla-style dense layout  
- Tiny mobile tap targets  
- Low contrast text on cream/mint backgrounds  
- Hiding phone number below fold on mobile  

---

## Пріоритет дизайну

1. **Mobile-first** contact conversion (phone + forms)  
2. **Trust** (years, team, lab, equipment)  
3. **Service discovery** (clear mega-menu)  
4. **Implantology promo** on homepage  
5. **Price transparency** (readable tables)  

---

## Як використовувати

| Інструмент | Порада |
|------------|--------|
| Open Design | Встав у `start_run` одним блоком або розбий: спочатку design system, потім Home |
| Figma AI | Додай «create component library first, then pages» |
| По екранах | Копіюй секцію «Сторінка N» + Global components |

**Рекомендований порядок генерації:** design system → головна desktop/mobile → header/footer components → решта ключових екранів.
