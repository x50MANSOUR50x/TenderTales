import requests
import os
import json

topic = "artificial intelligence OR machine learning OR generative ai OR openai OR anthropic OR nvidia OR chatgpt"
page_size = 20

def create_document(id, source, title, content, date):
    return {
        "id": id,
        "source": source,
        "title": title,
        "content": content,
        "date": date
    }

def collect_news(topic=topic, page_size=page_size):
    api_key = os.getenv("NEWS_API_KEY")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size
    }

    headers = {
        "X-Api-Key": api_key
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    articles = data["articles"]
    documents = []

    for i, article in enumerate(articles):
        document = create_document(
            id=f"news_{i+1:03d}",
            source=article["source"]["name"],
            title=article["title"],
            content=article.get("content") or "",
            date=article["publishedAt"]
        )

        documents.append(document)

    return documents

def save_documents(documents, filename="Data preprocessing/Data/sample_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=4)

def main():
    documents = collect_news(topic)

    print("Articles collected:", len(documents))

    save_documents(documents)

    print("Data saved successfully.")



if __name__ == "__main__":
    main()