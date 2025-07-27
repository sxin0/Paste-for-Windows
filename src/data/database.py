#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据存储模块 - 使用SQLite数据库
负责剪贴板数据的持久化存储
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..core.clipboard_manager import ClipboardItem


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # 默认数据库路径
            app_data_dir = Path.home() / "AppData" / "Local" / "PasteForWindows"
            app_data_dir.mkdir(parents=True, exist_ok=True)
            db_path = app_data_dir / "clipboard.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        try:
            self._connection = sqlite3.connect(str(self.db_path))
            self._connection.row_factory = sqlite3.Row  # 使结果可以通过列名访问
            
            # 创建表
            self._create_tables()
            
            # 设置外键约束
            self._connection.execute("PRAGMA foreign_keys = ON")
            
            print(f"数据库初始化成功: {self.db_path}")
            
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            raise
    
    def _create_tables(self):
        """创建数据库表"""
        cursor = self._connection.cursor()
        
        # 剪贴板项目表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clipboard_items (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                content_type TEXT NOT NULL DEFAULT 'text',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                access_count INTEGER DEFAULT 0,
                is_favorite BOOLEAN DEFAULT FALSE,
                tags TEXT DEFAULT '',
                metadata TEXT DEFAULT '{}'
            )
        """)
        
        # 标签表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#0078d4',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 项目标签关联表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_tags (
                item_id TEXT,
                tag_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES clipboard_items(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (item_id, tag_id)
            )
        """)
        
        # 设置表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 统计表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                total_items INTEGER DEFAULT 0,
                text_items INTEGER DEFAULT 0,
                link_items INTEGER DEFAULT 0,
                file_items INTEGER DEFAULT 0,
                code_items INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self._connection.commit()
    
    def save_item(self, item: ClipboardItem) -> bool:
        """保存剪贴板项目"""
        try:
            cursor = self._connection.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO clipboard_items 
                (id, content, content_type, created_at, updated_at, access_count, is_favorite, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id,
                item.content,
                item.content_type,
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
                item.access_count,
                item.is_favorite,
                item.tags,
                json.dumps(item.metadata)
            ))
            
            self._connection.commit()
            return True
            
        except Exception as e:
            print(f"保存项目失败: {e}")
            return False
    
    def get_item(self, item_id: str) -> Optional[ClipboardItem]:
        """获取指定项目"""
        try:
            cursor = self._connection.cursor()
            
            cursor.execute("""
                SELECT * FROM clipboard_items WHERE id = ?
            """, (item_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_item(row)
            return None
            
        except Exception as e:
            print(f"获取项目失败: {e}")
            return None
    
    def get_all_items(self, limit: int = None, offset: int = 0) -> List[ClipboardItem]:
        """获取所有项目"""
        try:
            cursor = self._connection.cursor()
            
            query = "SELECT * FROM clipboard_items ORDER BY updated_at DESC"
            params = []
            
            if limit:
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            items = []
            for row in cursor.fetchall():
                items.append(self._row_to_item(row))
            
            return items
            
        except Exception as e:
            print(f"获取所有项目失败: {e}")
            return []
    
    def get_recent_items(self, limit: int = 50) -> List[ClipboardItem]:
        """获取最近的项目"""
        return self.get_all_items(limit=limit)
    
    def get_favorite_items(self) -> List[ClipboardItem]:
        """获取收藏的项目"""
        try:
            cursor = self._connection.cursor()
            
            cursor.execute("""
                SELECT * FROM clipboard_items 
                WHERE is_favorite = TRUE 
                ORDER BY updated_at DESC
            """)
            
            items = []
            for row in cursor.fetchall():
                items.append(self._row_to_item(row))
            
            return items
            
        except Exception as e:
            print(f"获取收藏项目失败: {e}")
            return []
    
    def search_items(self, query: str, limit: int = 50) -> List[ClipboardItem]:
        """搜索项目"""
        try:
            cursor = self._connection.cursor()
            
            cursor.execute("""
                SELECT * FROM clipboard_items 
                WHERE content LIKE ? OR tags LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            items = []
            for row in cursor.fetchall():
                items.append(self._row_to_item(row))
            
            return items
            
        except Exception as e:
            print(f"搜索项目失败: {e}")
            return []
    
    def update_item(self, item: ClipboardItem) -> bool:
        """更新项目"""
        return self.save_item(item)
    
    def delete_item(self, item_id: str) -> bool:
        """删除项目"""
        try:
            cursor = self._connection.cursor()
            
            cursor.execute("DELETE FROM clipboard_items WHERE id = ?", (item_id,))
            
            self._connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"删除项目失败: {e}")
            return False
    
    def clear_all_items(self) -> bool:
        """清空所有项目"""
        try:
            cursor = self._connection.cursor()
            
            cursor.execute("DELETE FROM clipboard_items")
            
            self._connection.commit()
            return True
            
        except Exception as e:
            print(f"清空所有项目失败: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            cursor = self._connection.cursor()
            
            # 总项目数
            cursor.execute("SELECT COUNT(*) as total FROM clipboard_items")
            total_items = cursor.fetchone()['total']
            
            # 各类型项目数
            cursor.execute("""
                SELECT content_type, COUNT(*) as count 
                FROM clipboard_items 
                GROUP BY content_type
            """)
            content_types = dict(cursor.fetchall())
            
            # 收藏项目数
            cursor.execute("SELECT COUNT(*) as count FROM clipboard_items WHERE is_favorite = TRUE")
            favorite_count = cursor.fetchone()['count']
            
            # 最近7天的项目数
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM clipboard_items 
                WHERE created_at >= datetime('now', '-7 days')
            """)
            recent_week = cursor.fetchone()['count']
            
            return {
                'total_items': total_items,
                'content_types': content_types,
                'favorite_count': favorite_count,
                'recent_week': recent_week
            }
            
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {}
    
    def _row_to_item(self, row) -> ClipboardItem:
        """将数据库行转换为ClipboardItem对象"""
        return ClipboardItem(
            id=row['id'],
            content=row['content'],
            content_type=row['content_type'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
            access_count=row['access_count'],
            is_favorite=bool(row['is_favorite']),
            tags=row['tags'],
            metadata=json.loads(row['metadata'])
        )
    
    def close(self):
        """关闭数据库连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 