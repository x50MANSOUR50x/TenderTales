import re


def remove_duplicates(documents):
    unique_documents = []
    seen = set()

    for document in documents:
        key = (
            document.get("title", "").strip().lower(),
            document.get("content", "").strip().lower()
        )

        if key not in seen:
            seen.add(key)
            unique_documents.append(document)

    return unique_documents


def handle_missing_values(documents):
    for document in documents:
        document["title"] = document.get("title") or ""
        document["content"] = document.get("content") or ""
        document["date"] = document.get("date") or ""
        document["source"] = document.get("source") or "unknown"

    return documents


def clean_text(text):
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.,!?'-]", "", text)
    return text.strip()


def combine_title_content(documents):
    for document in documents:
        document["content"] = clean_text(
            document["title"] + " " + document["content"]
        )

    return documents


def preprocess_documents(documents):
    documents = handle_missing_values(documents)
    documents = remove_duplicates(documents)
    documents = combine_title_content(documents)

    return documents


if __name__ == "__main__":
    from data_collection import collect_sample_data

    documents = collect_sample_data()
    documents = preprocess_documents(documents)

    for document in documents:
        print(document)