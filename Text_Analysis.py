from textblob import TextBlob
from newspaper import Article

url = 'https://en.wikipedia.org/wiki/Lionel_Messi'

article = Article(url)
article.download()
article.parse()

# Skip .nlp() to avoid the punkt_tab issue
text = article.text
print("Full Text:\n", text[:500])  # Print a preview

blob = TextBlob(text)
sentiment = blob.sentiment.polarity
print("\nSentiment Polarity:", sentiment)
