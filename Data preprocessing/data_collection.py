def create_document(id, source, title, content, date):
    return {
        "id": id,
        "source": source,
        "title": title,
        "content": content,
        "date": date
    }


def collect_sample_data():
    documents = []

    documents.append(
        create_document(
            "news_001",
            "newsapi",
            "New AI Model Released",
            "A new artificial intelligence model has been released. https://example.com/news",
            "2026-09-07T12:00:00"
        )
    )

    documents.append(
        create_document(
            "news_002",
            "newsapi",
            "New AI Model Released",
            "A new artificial intelligence model has been released. https://example.com/news",
            "2026-09-07T12:00:00"
        )
    )

    documents.append(
        create_document(
            "reddit_001",
            "reddit",
            None,
            "People are discussing the new AI model on Reddit.",
            "2026-09-07T13:00:00"
        )
    )

    return documents


if __name__ == "__main__":
    documents = collect_sample_data()

    for document in documents:
        print(document)