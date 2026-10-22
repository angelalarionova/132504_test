import requests
from bs4 import BeautifulSoup
import csv

START_URL = "http://www.enron-mail.com/email/allen-p/"
OUT_FILE = "enron_1000.csv"
headers = {'User-Agent': 'Mozilla/5.0'}

# Очередь страниц, которые нужно посетить
queue = [START_URL]
# Множество посещенных страниц (чтобы не ходить по кругу)
visited = set()
# Список найденных писем
email_links = []

#ссылки на письма
while queue and len(email_links) < 1000:
    url = queue.pop(0)
    if url in visited:
        continue
    visited.add(url)

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            href = a['href']
            # Пропускаем ссылки "назад" и пустые
            if href in ['../', './', '/', '#'] or href.startswith('?'):
                continue

            full_url = url + href if not href.startswith('http') else href

            if href.endswith('.html'):
                # Это письмо —> добавляем в список
                if full_url not in email_links:
                    email_links.append(full_url)
            else:
                # Это папка —> добавляем в очередь на посещение
                if full_url not in visited and full_url not in queue:
                    queue.append(full_url)
    except Exception:
        pass


# парсим сами письма
with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["from", "to", "date", "subject", "body"])

    count = 0
    for url in email_links:
        try:
            page = requests.get(url, headers=headers, timeout=5)
            s = BeautifulSoup(page.text, 'html.parser')

            data = {}
            for tr in s.find_all('tr'):
                cols = tr.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].text.strip().replace(':', '')
                    if key in ['From', 'To', 'Subject', 'Date']:
                        data[key] = cols[1].text.strip()

            body = ""
            text = s.get_text()
            if "Subject:" in text and "Date:" in text:
                body = text.split("Date:")[-1].strip()[:1000]  # обрезаем тело до 1000 символов

            writer.writerow([
                data.get('From', ''),
                data.get('To', ''),
                data.get('Date', ''),
                data.get('Subject', ''),
                body
            ])

            count += 1
            if count % 100 == 0:
                print(f"Скачано: {count}...")

        except Exception:
            pass

print(f"\ncохранено в {OUT_FILE}: {count} писем.")