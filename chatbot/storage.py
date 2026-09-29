"""
Local SQLite persistence for conversation history.

Each person's chat is a "conversation": a row in `conversations` plus its
ordered `messages`. Kept separate per `user_name` so the sidebar only shows
that person's own past conversations.

NOTE: this is a local file (chatbot/conversations.db). On Streamlit Community
Cloud the container filesystem is wiped on every redeploy/reboot, so this
does NOT survive those - fine for a working prototype, not yet a system of
record. Swap for a hosted DB (e.g. Turso, Supabase) if that's ever needed;
the functions below are the only thing that would need to change.
"""
import json
import sqlite3
import time
import uuid
from pathlib import Path

DB_PATH = Path(__file__).parent / "conversations.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # reduces lock contention across concurrent users
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL REFERENCES conversations(id),
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            sources TEXT,
            frames TEXT,
            created_at REAL NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_name)")
    conn.commit()
    conn.close()


def create_conversation(user_name: str, title: str) -> str:
    conv_id = str(uuid.uuid4())
    now = time.time()
    conn = get_conn()
    conn.execute(
        "INSERT INTO conversations (id, user_name, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (conv_id, user_name, title[:80], now, now),
    )
    conn.commit()
    conn.close()
    return conv_id


def add_message(conversation_id: str, role: str, content: str, sources=None, frames=None):
    now = time.time()
    conn = get_conn()
    conn.execute(
        "INSERT INTO messages (conversation_id, role, content, sources, frames, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            conversation_id,
            role,
            content,
            json.dumps(sources) if sources is not None else None,
            json.dumps(frames) if frames is not None else None,
            now,
        ),
    )
    conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    conn.commit()
    conn.close()


def list_conversations(user_name: str, limit: int = 50):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, title, updated_at FROM conversations WHERE user_name = ? "
        "ORDER BY updated_at DESC LIMIT ?",
        (user_name, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_messages(conversation_id: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT role, content, sources, frames FROM messages "
        "WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,),
    ).fetchall()
    conn.close()
    out = []
    for r in rows:
        msg = {"role": r["role"], "content": r["content"]}
        if r["sources"]:
            msg["sources"] = json.loads(r["sources"])
        if r["frames"]:
            msg["frames"] = json.loads(r["frames"])
        out.append(msg)
    return out


def delete_conversation(conversation_id: str):
    conn = get_conn()
    conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()


def rename_conversation(conversation_id: str, title: str):
    conn = get_conn()
    conn.execute("UPDATE conversations SET title = ? WHERE id = ?", (title[:80], conversation_id))
    conn.commit()
    conn.close()
