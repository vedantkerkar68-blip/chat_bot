import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Tuple, Optional
import os

class DatabaseManager:
    def __init__(self, db_path: str = "chatbot_history.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the history table if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_query TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    query_type TEXT DEFAULT 'text',
                    image_path TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Database initialized successfully!")
            
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
    
    def add_conversation(self, user_query: str, ai_response: str, query_type: str = 'text', image_path: str = None) -> bool:
        """Add a new conversation entry to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO history (user_query, ai_response, query_type, image_path)
                VALUES (?, ?, ?, ?)
            ''', (user_query, ai_response, query_type, image_path))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Error adding conversation: {e}")
            return False
    
    def get_all_conversations(self, limit: int = None) -> List[Tuple]:
        """Retrieve all conversations from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if limit:
                cursor.execute('''
                    SELECT id, user_query, ai_response, timestamp, query_type, image_path
                    FROM history 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            else:
                cursor.execute('''
                    SELECT id, user_query, ai_response, timestamp, query_type, image_path
                    FROM history 
                    ORDER BY timestamp DESC
                ''')
            
            conversations = cursor.fetchall()
            conn.close()
            return conversations
            
        except sqlite3.Error as e:
            print(f"Error retrieving conversations: {e}")
            return []
    
    def search_conversations(self, search_term: str) -> List[Tuple]:
        """Search for conversations containing the search term."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, user_query, ai_response, timestamp, query_type, image_path
                FROM history 
                WHERE user_query LIKE ? OR ai_response LIKE ?
                ORDER BY timestamp DESC
            ''', (f'%{search_term}%', f'%{search_term}%'))
            
            results = cursor.fetchall()
            conn.close()
            return results
            
        except sqlite3.Error as e:
            print(f"Error searching conversations: {e}")
            return []
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a specific conversation by ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM history WHERE id = ?', (conversation_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    def clear_all_history(self) -> bool:
        """Clear all conversation history."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM history')
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Error clearing history: {e}")
            return False
    
    
    def get_conversation_stats(self) -> dict:
        """Get statistics about conversations."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total conversations
            cursor.execute('SELECT COUNT(*) FROM history')
            total = cursor.fetchone()[0]
            
            # Conversations by type
            cursor.execute('''
                SELECT query_type, COUNT(*) 
                FROM history 
                GROUP BY query_type
            ''')
            by_type = dict(cursor.fetchall())
            
            # Recent conversations (last 7 days)
            cursor.execute('''
                SELECT COUNT(*) 
                FROM history 
                WHERE datetime(timestamp) > datetime('now', '-7 days')
            ''')
            recent = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_conversations': total,
                'by_type': by_type,
                'recent_conversations': recent
            }
            
        except sqlite3.Error as e:
            print(f"Error getting stats: {e}")
            return {}

if __name__ == "__main__":
    # Test the database functionality
    db = DatabaseManager()
    
    # Test adding a conversation
    db.add_conversation(
        user_query="Hello, how are you?",
        ai_response="Hello! I'm doing well, thank you for asking. How can I help you today?",
        query_type="text"
    )
    
    # Test retrieving conversations
    conversations = db.get_all_conversations(limit=5)
    print("Recent conversations:")
    for conv in conversations:
        print(f"User: {conv[1]}")
        print(f"AI: {conv[2]}")
        print(f"Time: {conv[3]}")
        print("-" * 50)