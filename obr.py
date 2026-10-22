import pandas as pd
import re

df = pd.read_csv('enron_1000.csv', sep=';', encoding='utf-8')

# Удаляем пустые письма
df = df.dropna(subset=['body', 'subject'])

print(f"Писем до очистки: {len(df)}")


#ункция очистки
def clean_text(text):
    if not isinstance(text, str):
        return ""

    # Удаляем HTML теги (если есть)
    text = re.sub(r'<.*?>', ' ', text)

    # Удаляем email-адреса (типа user@enron.com)
    text = re.sub(r'\S+@\S+', ' ', text)

    # Удаляем ссылки (начинающиеся с http, www или просто домены)
    text = re.sub(r'http\S+|www\.\S+', ' ', text)

    # Удаляем даты (например, 04/04/2001 или Wed, 4 Apr 2001)
    text = re.sub(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', ' ', text)
    text = re.sub(
        r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s+\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
        ' ', text)

    # Удаляем длинные цепочки дефисов, звездочек, тильд (типа --- Forwarded by ---)
    text = re.sub(r'[-=~_*]{2,}', ' ', text)

    # Оставляем ТОЛЬКО английские буквы и пробелы
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Приводим к нижнему регистру
    text = text.lower()

    # Разбиваем на слова
    words = text.split()

    # Список стоп-слов
    stopwords = set(['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
                     'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
                     'to', 'was', 'were', 'will', 'with', 'this', 'but', 'they', 'i',
                     'you', 'we', 'my', 'me', 'our', 'us', 'if', 'or', 'so', 'do', 'com', 'ect'])

    # Оставляем слова длиной от 3 символов и убираем стоп-слова
    clean_words = [w for w in words if w not in stopwords and len(w) > 2]

    return " ".join(clean_words)

# Применяем очистку к Subject и Body
df['clean_subject'] = df['subject'].apply(clean_text)
df['clean_body'] = df['body'].apply(clean_text)

# . Оставляем только нужные колонки
result_df = df[['clean_subject', 'clean_body']]

result_df.to_csv('enron_final.csv', sep=';', index=False, encoding='utf-8')
print("\nenron_final.csv")
