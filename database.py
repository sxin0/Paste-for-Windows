"""
剪贴板历史数据库管理
"""
import sqlite3
import json
import datetime
from typing import List, Dict, Any, Optional
from config import DB_PATH, config

class ClipboardDatabase:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 创建剪贴板历史表
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clipboard_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        content_type TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        size INTEGER DEFAULT 0,
                        metadata TEXT DEFAULT '{}',
                        is_favorite INTEGER DEFAULT 0,
                        created_at TEXT NOT NULL,
                        accessed_count INTEGER DEFAULT 0,
                        last_accessed TEXT
                    )
                ''')
                
                # 创建索引以提高查询性能
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_timestamp 
                    ON clipboard_history(timestamp)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_content_type 
                    ON clipboard_history(content_type)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_is_favorite 
                    ON clipboard_history(is_favorite)
                ''')
                
                conn.commit()
        except Exception as e:
            print(f"数据库初始化失败: {e}")
    
    def add_clipboard_item(self, content: str, content_type: str, metadata: Dict = None) -> bool:
        """添加剪贴板项目"""
        try:
            if metadata is None:
                metadata = {}
            
            now = datetime.datetime.now().isoformat()
            size = len(content.encode('utf-8'))
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 检查是否已存在相同内容
                cursor.execute(
                    "SELECT id FROM clipboard_history WHERE content = ? ORDER BY timestamp DESC LIMIT 1",
                    (content,)
                )
                existing = cursor.fetchone()
                
                if existing:
                    # 更新已存在项目的时间戳
                    cursor.execute(
                        "UPDATE clipboard_history SET timestamp = ?, accessed_count = accessed_count + 1, last_accessed = ? WHERE id = ?",
                        (now, now, existing[0])
                    )
                else:
                    # 插入新项目
                    cursor.execute('''
                        INSERT INTO clipboard_history 
                        (content, content_type, timestamp, size, metadata, created_at, last_accessed)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (content, content_type, now, size, json.dumps(metadata), now, now))
                
                conn.commit()
                
                # 清理旧数据
                self.cleanup_old_items()
                
                return True
        except Exception as e:
            print(f"添加剪贴板项目失败: {e}")
            return False
    
    def get_clipboard_history(self, limit: int = None, content_type: str = None) -> List[Dict[str, Any]]:
        """获取剪贴板历史"""
        try:
            if limit is None:
                limit = config.getint("general", "max_history_items", 100)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM clipboard_history"
                params = []
                
                if content_type:
                    query += " WHERE content_type = ?"
                    params.append(content_type)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # 转换为字典格式
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in rows:
                    item = dict(zip(columns, row))
                    try:
                        item['metadata'] = json.loads(item['metadata'])
                    except:
                        item['metadata'] = {}
                    results.append(item)
                
                return results
        except Exception as e:
            print(f"获取剪贴板历史失败: {e}")
            return []
    
    def search_clipboard_history(self, keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索剪贴板历史"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM clipboard_history 
                    WHERE content LIKE ? 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (f'%{keyword}%', limit))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                results = []
                for row in rows:
                    item = dict(zip(columns, row))
                    try:
                        item['metadata'] = json.loads(item['metadata'])
                    except:
                        item['metadata'] = {}
                    results.append(item)
                
                return results
        except Exception as e:
            print(f"搜索剪贴板历史失败: {e}")
            return []
    
    def delete_clipboard_item(self, item_id: int) -> bool:
        """删除剪贴板项目"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clipboard_history WHERE id = ?", (item_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"删除剪贴板项目失败: {e}")
            return False
    
    def clear_all_history(self) -> bool:
        """清空所有历史记录"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clipboard_history")
                conn.commit()
                return True
        except Exception as e:
            print(f"清空历史记录失败: {e}")
            return False
    
    def toggle_favorite(self, item_id: int) -> bool:
        """切换收藏状态"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE clipboard_history 
                    SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END 
                    WHERE id = ?
                ''', (item_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"切换收藏状态失败: {e}")
            return False
    
    def cleanup_old_items(self):
        """清理旧的剪贴板项目"""
        try:
            max_items = config.getint("general", "max_history_items", 100)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 保留收藏项目和最新的项目
                cursor.execute('''
                    DELETE FROM clipboard_history 
                    WHERE id NOT IN (
                        SELECT id FROM clipboard_history 
                        WHERE is_favorite = 1
                        UNION
                        SELECT id FROM clipboard_history 
                        ORDER BY timestamp DESC LIMIT ?
                    )
                ''', (max_items,))
                
                conn.commit()
        except Exception as e:
            print(f"清理旧项目失败: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 总项目数
                cursor.execute("SELECT COUNT(*) FROM clipboard_history")
                total_items = cursor.fetchone()[0]
                
                # 收藏项目数
                cursor.execute("SELECT COUNT(*) FROM clipboard_history WHERE is_favorite = 1")
                favorite_items = cursor.fetchone()[0]
                
                # 各类型项目数
                cursor.execute('''
                    SELECT content_type, COUNT(*) 
                    FROM clipboard_history 
                    GROUP BY content_type
                ''')
                type_stats = dict(cursor.fetchall())
                
                # 今日新增项目数
                today = datetime.date.today().isoformat()
                cursor.execute('''
                    SELECT COUNT(*) FROM clipboard_history 
                    WHERE DATE(created_at) = ?
                ''', (today,))
                today_items = cursor.fetchone()[0]
                
                return {
                    'total_items': total_items,
                    'favorite_items': favorite_items,
                    'type_statistics': type_stats,
                    'today_items': today_items
                }
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {} 