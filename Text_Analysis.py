from newspaper import Article
from textblob import TextBlob
import nltk
import matplotlib.pyplot as plt

# Download NLTK's sentence tokenizer
nltk.download('punkt')

# URL of the article
url = 'https://en.wikipedia.org/wiki/Lionel_Messi'

# Load and parse the article
article = Article(url)
article.download()
article.parse()

# Extract the article text
text = article.text

# Analyze sentiment at sentence level
blob = TextBlob(text)
sentences = blob.sentences

print("\n====== Sentence-level Sentiment Analysis (First 10 Sentences) ======\n")
for i, sentence in enumerate(sentences[:10]):
    print(f"Sentence {i+1}: {sentence}")
    print(f"→ Polarity: {sentence.sentiment.polarity:.2f}, Subjectivity: {sentence.sentiment.subjectivity:.2f}\n")

# Identify most positive and most negative sentences
sorted_sentences = sorted(sentences, key=lambda s: s.sentiment.polarity)

print("====== Most Negative Sentence ======\n")
print(sorted_sentences[0])
print("→ Polarity:", sorted_sentences[0].sentiment.polarity)

print("\n====== Most Positive Sentence ======\n")
print(sorted_sentences[-1])
print("→ Polarity:", sorted_sentences[-1].sentiment.polarity)

# Classify overall sentiment
def classify_sentiment(p):
    if p > 0.1:
        return "Positive"
    elif p < -0.1:
        return "Negative"
    else:
        return "Neutral"

overall_polarity = blob.sentiment.polarity
print(f"\n====== Overall Article Sentiment ======\n→ Polarity Score: {overall_polarity:.2f}")
print(f"→ Classified as: {classify_sentiment(overall_polarity)}")

# Visualize sentiment trend
polarities = [s.sentiment.polarity for s in sentences]

plt.figure(figsize=(12, 5))
plt.plot(polarities, marker='o', linestyle='-', color='blue')
plt.title("Sentiment Polarity per Sentence")
plt.xlabel("Sentence Number")
plt.ylabel("Polarity Score")
plt.axhline(0, color='gray', linestyle='--')  # Neutral line
plt.grid(True)
plt.tight_layout()
plt.show()

