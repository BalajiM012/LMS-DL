import pandas as pd
import numpy as np
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

class BookAnalyzer:
    def __init__(self):
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
        
    def analyze_book_sentiment(self, text):
        """Analyze sentiment of book descriptions/reviews"""
        if not text or pd.isna(text):
            return {'compound': 0, 'positive': 0, 'neutral': 0, 'negative': 0}
        
        sentiment = self.sia.polarity_scores(str(text))
        return {
            'compound': sentiment['compound'],
            'positive': sentiment['pos'],
            'neutral': sentiment['neu'],
            'negative': sentiment['neg']
        }
    
    def extract_topics(self, texts, n_topics=5):
        """Extract topics from book descriptions using LDA"""
        if not texts or all(pd.isna(text) for text in texts):
            return []
        
        # Clean and prepare texts
        clean_texts = [str(text) for text in texts if text and not pd.isna(text)]
        if not clean_texts:
            return []
        
        # Vectorize texts
        vectorizer = CountVectorizer(max_features=100, stop_words='english')
        doc_term_matrix = vectorizer.fit_transform(clean_texts)
        
        # Apply LDA
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(doc_term_matrix)
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-5:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics.append({
                'topic_id': topic_idx,
                'words': top_words,
                'weights': topic[top_words_idx].tolist()
            })
        
        return topics
    
    def analyze_reading_patterns(self, borrow_records):
        """Analyze user reading patterns"""
        if not borrow_records:
            return {}
        
        df = pd.DataFrame(borrow_records)
        
        # Genre preferences
        genre_counts = df['genre'].value_counts().to_dict()
        
        # Reading frequency
        df['borrow_date'] = pd.to_datetime(df['borrow_date'])
        df['month'] = df['borrow_date'].dt.to_period('M')
        monthly_reading = df.groupby('month').size().to_dict()
        
        # Popular books
        popular_books = df['book_id'].value_counts().head(10).to_dict()
        
        # Average reading time
        if 'return_date' in df.columns:
            df['return_date'] = pd.to_datetime(df['return_date'])
            df['reading_days'] = (df['return_date'] - df['borrow_date']).dt.days
            avg_reading_time = df['reading_days'].mean()
        else:
            avg_reading_time = None
        
        return {
            'genre_preferences': genre_counts,
            'monthly_reading': monthly_reading,
            'popular_books': popular_books,
            'avg_reading_days': avg_reading_time
        }
    
    def generate_book_insights(self, books_df):
        """Generate insights from book collection"""
        insights = {
            'total_books': len(books_df),
            'genres': books_df['genre'].nunique(),
            'authors': books_df['author'].nunique(),
            'avg_rating': books_df['average_rating'].mean(),
            'total_pages': books_df['pages'].sum(),
            'year_range': {
                'oldest': books_df['year'].min(),
                'newest': books_df['year'].max()
            }
        }
        
        # Sentiment analysis
        books_df['sentiment'] = books_df['description'].apply(
            lambda x: self.analyze_book_sentiment(x)['compound']
        )
        insights['sentiment_stats'] = {
            'positive_books': len(books_df[books_df['sentiment'] > 0.1]),
            'neutral_books': len(books_df[(books_df['sentiment'] >= -0.1) & (books_df['sentiment'] <= 0.1)]),
            'negative_books': len(books_df[books_df['sentiment'] < -0.1])
        }
        
        # Genre distribution
        genre_stats = books_df.groupby('genre').agg({
            'average_rating': 'mean',
            'pages': 'mean',
            'sentiment': 'mean'
        }).round(2)
        insights['genre_stats'] = genre_stats.to_dict()
        
        return insights
    
    def predict_popularity(self, book_features):
        """Predict book popularity based on features"""
        # Simple popularity score based on multiple factors
        features = {
            'rating': book_features.get('average_rating', 0),
            'pages': book_features.get('pages', 0),
            'year': book_features.get('year', 2000),
            'sentiment': self.analyze_book_sentiment(book_features.get('description', ''))['compound']
        }
        
        # Normalize features
        normalized_rating = min(features['rating'] / 5.0, 1.0)
        normalized_pages = min(features['pages'] / 1000.0, 1.0)
        normalized_year = max(0, (features['year'] - 1900) / 120.0)
        normalized_sentiment = (features['sentiment'] + 1) / 2.0
        
        # Calculate popularity score
        popularity_score = (
            normalized_rating * 0.4 +
            normalized_sentiment * 0.3 +
            normalized_year * 0.2 +
            (1 - normalized_pages) * 0.1
        )
        
        return {
            'popularity_score': round(popularity_score, 3),
            'factors': {
                'rating_factor': normalized_rating,
                'sentiment_factor': normalized_sentiment,
                'recency_factor': normalized_year,
                'length_factor': 1 - normalized_pages
            }
        }
    
    def create_visualizations(self, books_df, save_path='static/images/'):
        """Create data visualizations"""
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        os.makedirs(save_path, exist_ok=True)
        
        # Genre distribution
        plt.figure(figsize=(12, 6))
        genre_counts = books_df['genre'].value_counts()
        plt.pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%')
        plt.title('Book Genre Distribution')
        plt.savefig(os.path.join(save_path, 'genre_distribution.png'))
        plt.close()
        
        # Rating vs Year scatter plot
        plt.figure(figsize=(12, 6))
        plt.scatter(books_df['year'], books_df['average_rating'], alpha=0.6)
        plt.xlabel('Year')
        plt.ylabel('Average Rating')
        plt.title('Book Ratings Over Time')
        plt.savefig(os.path.join(save_path, 'rating_trend.png'))
        plt.close()
        
        # Pages distribution
        plt.figure(figsize=(12, 6))
        plt.hist(books_df['pages'], bins=20, edgecolor='black')
        plt.xlabel('Pages')
        plt.ylabel('Count')
        plt.title('Book Length Distribution')
        plt.savefig(os.path.join(save_path, 'pages_distribution.png'))
        plt.close()
        
        return {
            'genre_chart': 'genre_distribution.png',
            'rating_trend': 'rating_trend.png',
            'pages_chart': 'pages_distribution.png'
        }
