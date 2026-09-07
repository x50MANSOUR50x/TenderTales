from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from datetime import datetime, timezone
import re

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "has", "have", "had", "been", "be",
    "in", "on", "at", "to", "of", "for", "from",
    "and", "or", "but", "with", "as", "by",
    "this", "that", "these", "those",
    "it", "its", "they", "them", "their",
    "he", "she", "we", "you", "i"
}


def calculate_frequency(documents):
    word_counts = Counter()

    for document in documents:
        text = document["content"].lower()
        words = re.findall(r"\b[a-zA-Z]+\b", text)

        for word in words:
            if word not in STOP_WORDS:
                word_counts[word] += 1

    return word_counts


def calculate_recency(documents):
    now = datetime.now(timezone.utc)
    recency_scores = {}

    for document in documents:
        date = datetime.fromisoformat(document["date"]).replace(tzinfo=timezone.utc)
        age_hours = max((now - date).total_seconds() / 3600, 0)
        score = 1 / (1 + age_hours)

        recency_scores[document["id"]] = score

    return recency_scores


def extract_keywords(documents, top_k=5):
    texts = [document["content"] for document in documents]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(texts)
    features = vectorizer.get_feature_names_out()

    keyword_scores = {}

    for index in range(len(documents)):
        scores = matrix[index].toarray().flatten()

        for feature_index, score in enumerate(scores):
            if score > 0:
                keyword = features[feature_index]
                keyword_scores[keyword] = keyword_scores.get(keyword, 0) + score

    ranked_keywords = sorted(
        keyword_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_keywords[:top_k]


def calculate_source_diversity(documents, keywords):
    diversity = {}

    for keyword, _ in keywords:
        sources = set()

        for document in documents:
            text = document["content"].lower()

            if keyword.lower() in text:
                sources.add(document["source"])

        diversity[keyword] = len(sources)

    return diversity


def calculate_keyword_recency(documents, keywords, recency_scores):
    keyword_recency = {}

    for keyword, _ in keywords:
        scores = []

        for document in documents:
            if keyword.lower() in document["content"].lower():
                scores.append(recency_scores[document["id"]])

        if scores:
            keyword_recency[keyword] = sum(scores) / len(scores)
        else:
            keyword_recency[keyword] = 0

    return keyword_recency


def normalize_scores(scores):
    max_score = max(scores.values())

    if max_score == 0:
        return {key: 0 for key in scores}

    return {
        key: value / max_score
        for key, value in scores.items()
    }

def calculate_trend_scores(frequency, keyword_recency, source_diversity):
    keyword_frequency = {
        keyword: frequency.get(keyword, 0)
        for keyword in source_diversity
    }

    normalized_frequency = normalize_scores(keyword_frequency)
    normalized_recency = normalize_scores(keyword_recency)
    normalized_diversity = normalize_scores(source_diversity)

    trend_scores = {}

    for keyword in source_diversity:
        trend_scores[keyword] = (
            normalized_frequency[keyword] * 0.4
            + normalized_recency[keyword] * 0.3
            + normalized_diversity[keyword] * 0.3
        )

    return trend_scores

def get_top_trends(trend_scores, top_k=3):
    ranked_trends = sorted(
        trend_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_trends[:top_k]



if __name__ == "__main__":
    from data_collection import collect_sample_data
    from preprocessing import preprocess_documents

    documents = collect_sample_data()
    documents = preprocess_documents(documents)

    frequency = calculate_frequency(documents)
    recency = calculate_recency(documents)
    keywords = extract_keywords(documents)
    source_diversity = calculate_source_diversity(documents, keywords)

    keyword_recency = calculate_keyword_recency(
        documents,
        keywords,
        recency
    )

    trend_scores = calculate_trend_scores(
        frequency,
        keyword_recency,
        source_diversity
    )

    top_trends = get_top_trends(trend_scores)

    print("Frequency:")
    print(frequency)

    print("Recency:")
    print(recency)

    print("Keywords:")
    print(keywords)

    print("Source Diversity:")
    print(source_diversity)

    print("Keyword Recency:")
    print(keyword_recency)

    print("Trend Scores:")
    print(trend_scores)

    print("Top Trends:")
    print(top_trends)