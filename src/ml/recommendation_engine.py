import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Flatten, Concatenate, Dropout
from tensorflow.keras.optimizers import Adam
import pickle
import os

class BookRecommendationEngine:
    def __init__(self):
        self.content_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.collaborative_model = None
        self.content_similarity_matrix = None
        self.svd_model = TruncatedSVD(n_components=50, random_state=42)
        self.scaler = StandardScaler()
        
    def prepare_content_features(self, books_df):
        """Prepare content-based features from book metadata"""
        # Combine text features
        books_df['content_features'] = (
            books_df['title'].fillna('') + ' ' +
            books_df['author'].fillna('') + ' ' +
            books_df['genre'].fillna('') + ' ' +
            books_df['description'].fillna('')
        )
        
        # Create TF-IDF matrix
        content_matrix = self.content_vectorizer.fit_transform(books_df['content_features'])
        self.content_similarity_matrix = cosine_similarity(content_matrix)
        
        return content_matrix
    
    def build_collaborative_model(self, n_users, n_books, embedding_dim=50):
        """Build neural collaborative filtering model"""
        # User embedding
        user_input = Input(shape=(1,), name='user_input')
        user_embedding = Embedding(n_users, embedding_dim, name='user_embedding')(user_input)
        user_vec = Flatten(name='user_flatten')(user_embedding)
        
        # Book embedding
        book_input = Input(shape=(1,), name='book_input')
        book_embedding = Embedding(n_books, embedding_dim, name='book_embedding')(book_input)
        book_vec = Flatten(name='book_flatten')(book_embedding)
        
        # Concatenate embeddings
        concat = Concatenate(name='concatenation')([user_vec, book_vec])
        
        # Dense layers
        dense1 = Dense(128, activation='relu', name='dense1')(concat)
        dropout1 = Dropout(0.5, name='dropout1')(dense1)
        dense2 = Dense(64, activation='relu', name='dense2')(dropout1)
        dropout2 = Dropout(0.5, name='dropout2')(dense2)
        dense3 = Dense(32, activation='relu', name='dense3')(dropout2)
        
        # Output layer
        output = Dense(1, activation='sigmoid', name='output')(dense3)
        
        model = Model(inputs=[user_input, book_input], outputs=output)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        
        self.collaborative_model = model
        return model
    
    def train_collaborative_model(self, user_book_ratings):
        """Train the collaborative filtering model"""
        if self.collaborative_model is None:
            n_users = user_book_ratings['user_id'].nunique()
            n_books = user_book_ratings['book_id'].nunique()
            self.build_collaborative_model(n_users, n_books)
        
        # Prepare training data
        X_user = user_book_ratings['user_id'].values
        X_book = user_book_ratings['book_id'].values
        y = user_book_ratings['rating'].values
        
        # Train model
        history = self.collaborative_model.fit(
            [X_user, X_book], y,
            batch_size=32,
            epochs=10,
            validation_split=0.2,
            verbose=1
        )
        
        return history
    
    def get_content_based_recommendations(self, book_id, books_df, top_n=10):
        """Get content-based recommendations"""
        if self.content_similarity_matrix is None:
            self.prepare_content_features(books_df)
        
        book_idx = books_df[books_df['id'] == book_id].index[0]
        similar_books = list(enumerate(self.content_similarity_matrix[book_idx]))
        similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)[1:top_n+1]
        
        recommendations = []
        for idx, score in similar_books:
            book = books_df.iloc[idx]
            recommendations.append({
                'book_id': int(book['id']),
                'title': book['title'],
                'author': book['author'],
                'score': float(score),
                'type': 'content_based'
            })
        
        return recommendations
    
    def get_collaborative_recommendations(self, user_id, books_df, top_n=10):
        """Get collaborative filtering recommendations"""
        if self.collaborative_model is None:
            return []
        
        # Get all book IDs
        all_book_ids = books_df['id'].values
        
        # Create predictions for all books
        user_array = np.array([user_id] * len(all_book_ids))
        predictions = self.collaborative_model.predict([user_array, all_book_ids])
        
        # Get top N recommendations
        book_scores = list(zip(all_book_ids, predictions.flatten()))
        book_scores = sorted(book_scores, key=lambda x: x[1], reverse=True)[:top_n]
        
        recommendations = []
        for book_id, score in book_scores:
            book = books_df[books_df['id'] == book_id].iloc[0]
            recommendations.append({
                'book_id': int(book_id),
                'title': book['title'],
                'author': book['author'],
                'score': float(score),
                'type': 'collaborative'
            })
        
        return recommendations
    
    def get_hybrid_recommendations(self, user_id, book_id, books_df, user_book_ratings, top_n=10):
        """Get hybrid recommendations combining content and collaborative filtering"""
        content_recs = self.get_content_based_recommendations(book_id, books_df, top_n)
        collab_recs = self.get_collaborative_recommendations(user_id, books_df, top_n)
        
        # Combine and rank recommendations
        all_recs = content_recs + collab_recs
        
        # Remove duplicates and sort by score
        unique_recs = {}
        for rec in all_recs:
            if rec['book_id'] not in unique_recs:
                unique_recs[rec['book_id']] = rec
            else:
                # Average scores for duplicates
                unique_recs[rec['book_id']]['score'] = (
                    unique_recs[rec['book_id']]['score'] + rec['score']
                ) / 2
        
        # Sort by score and return top N
        hybrid_recs = sorted(unique_recs.values(), key=lambda x: x['score'], reverse=True)[:top_n]
        
        return hybrid_recs
    
    def save_models(self, filepath='models/'):
        """Save trained models"""
        os.makedirs(filepath, exist_ok=True)
        
        # Save vectorizer
        with open(os.path.join(filepath, 'content_vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.content_vectorizer, f)
        
        # Save collaborative model
        if self.collaborative_model:
            self.collaborative_model.save(os.path.join(filepath, 'collaborative_model.h5'))
        
        # Save SVD model
        with open(os.path.join(filepath, 'svd_model.pkl'), 'wb') as f:
            pickle.dump(self.svd_model, f)
    
    def load_models(self, filepath='models/'):
        """Load trained models"""
        try:
            # Load vectorizer
            with open(os.path.join(filepath, 'content_vectorizer.pkl'), 'rb') as f:
                self.content_vectorizer = pickle.load(f)
            
            # Load collaborative model
            if os.path.exists(os.path.join(filepath, 'collaborative_model.h5')):
                self.collaborative_model = tf.keras.models.load_model(
                    os.path.join(filepath, 'collaborative_model.h5')
                )
            
            # Load SVD model
            with open(os.path.join(filepath, 'svd_model.pkl'), 'rb') as f:
                self.svd_model = pickle.load(f)
                
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
