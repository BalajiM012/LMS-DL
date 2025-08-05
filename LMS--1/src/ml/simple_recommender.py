import json
import math
from collections import defaultdict
from typing import List, Dict, Any

class SimpleRecommender:
    """Lightweight recommendation engine using pure Python"""
    
    def __init__(self):
        self.books = []
        self.user_ratings = defaultdict(dict)
        
    def load_books(self, books_data: List[Dict[str, Any]]):
        """Load book data"""
        self.books = books_data
        
    def add_rating(self, user_id: int, book_id: int, rating: float):
        """Add user rating"""
        self.user_ratings[user_id][book_id] = rating
        
    def get_content_based_recommendations(self, book_id: int, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get content-based recommendations using simple similarity"""
        target_book = None
        for book in self.books:
            if book['id'] == book_id:
                target_book = book
                break
                
        if not target_book:
            return []
            
        # Simple similarity based on genre and author
        recommendations = []
        for book in self.books:
            if book['id'] != book_id:
                score = 0
                
                # Genre similarity
                if book['genre'] == target_book['genre']:
                    score += 0.5
                    
                # Author similarity
                if book['author'] == target_book['author']:
                    score += 0.3
                    
                # Year similarity (within 5 years)
                year_diff = abs(book['year'] - target_book['year'])
                if year_diff <= 5:
                    score += 0.2
                    
                if score > 0:
                    recommendations.append({
                        'book': book,
                        'score': score,
                        'type': 'content_based'
                    })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]
    
    def get_popular_books(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Get popular books based on average ratings"""
        book_ratings = defaultdict(list)
        
        # Collect all ratings for each book
        for user_id, ratings in self.user_ratings.items():
            for book_id, rating in ratings.items():
                book_ratings[book_id].append(rating)
        
        # Calculate average ratings
        popular_books = []
        for book in self.books:
            book_id = book['id']
            if book_id in book_ratings:
                avg_rating = sum(book_ratings[book_id]) / len(book_ratings[book_id])
                popular_books.append({
                    'book': book,
                    'average_rating': avg_rating,
                    'rating_count': len(book_ratings[book_id])
                })
        
        # Sort by average rating
        popular_books.sort(key=lambda x: x['average_rating'], reverse=True)
        return popular_books[:top_n]
    
    def get_recommendations_for_user(self, user_id: int, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get recommendations for a specific user"""
        if user_id not in self.user_ratings:
            # Return popular books for new users
            return self.get_popular_books(top_n)
        
        user_books = set(self.user_ratings[user_id].keys())
        
        # Find similar users
        similar_users = []
        for other_user_id, ratings in self.user_ratings.items():
            if other_user_id != user_id:
                common_books = set(ratings.keys()) & user_books
                if common_books:
                    similarity = 0
                    for book_id in common_books:
                        similarity += 1 - abs(
                            self.user_ratings[user_id][book_id] - 
                            ratings[book_id]
                        ) / 5.0
                    
                    if similarity > 0:
                        similar_users.append((other_user_id, similarity))
        
        # Get recommendations from similar users
        recommendations = []
        book_scores = defaultdict(float)
        
        for other_user_id, similarity in similar_users:
            for book_id, rating in self.user_ratings[other_user_id].items():
                if book_id not in user_books:
                    book_scores[book_id] += rating * similarity
        
        # Get book details
        for book_id, score in book_scores.items():
            book = next((b for b in self.books if b['id'] == book_id), None)
            if book:
                recommendations.append({
                    'book': book,
                    'score': score,
                    'type': 'collaborative'
                })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]
    
    def search_books(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Simple search functionality"""
        query = query.lower()
        results = []
        
        for book in self.books:
            score = 0
            
            # Search in title
            if query in book['title'].lower():
                score += 2
                
            # Search in author
            if query in book['author'].lower():
                score += 1.5
                
            # Search in description
            if 'description' in book and query in book['description'].lower():
                score += 1
                
            # Search in genre
            if query in book['genre'].lower():
                score += 0.5
            
            if score > 0:
                book_copy = book.copy()
                book_copy['search_score'] = score
                results.append(book_copy)
        
        # Sort by search score
        results.sort(key=lambda x: x['search_score'], reverse=True)
        return results[:limit]
    
    def get_book_insights(self) -> Dict[str, Any]:
        """Get basic insights about the book collection"""
        if not self.books:
            return {}
        
        genres = defaultdict(int)
        authors = defaultdict(int)
        years = []
        ratings = []
        
        for book in self.books:
            genres[book['genre']] += 1
            authors[book['author']] += 1
            years.append(book['year'])
            if 'average_rating' in book:
                ratings.append(book['average_rating'])
        
        return {
            'total_books': len(self.books),
            'total_genres': len(genres),
            'total_authors': len(authors),
            'year_range': {
                'min': min(years) if years else 0,
                'max': max(years) if years else 0
            },
            'average_rating': sum(ratings) / len(ratings) if ratings else 0,
            'genre_distribution': dict(genres),
            'top_authors': dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5])
        }
