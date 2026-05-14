import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "prompt_lab.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            provider TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            version INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prompt_id) REFERENCES prompts(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            model_id INTEGER NOT NULL,
            input_text TEXT,
            output_text TEXT,
            latency_ms REAL,
            tokens_used INTEGER,
            status TEXT DEFAULT 'pending',
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prompt_id) REFERENCES prompts(id),
            FOREIGN KEY (model_id) REFERENCES models(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id INTEGER NOT NULL UNIQUE,
            response_time_ms REAL,
            token_count INTEGER,
            cost_usd REAL,
            quality_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (experiment_id) REFERENCES experiments(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            row_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def create_prompt(name: str, content: str, description: str = None) -> int:
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO prompts (name, content, description) VALUES (?, ?, ?)",
        (name, content, description)
    )
    conn.commit()
    prompt_id = cursor.lastrowid
    conn.close()
    return prompt_id

def get_prompt(prompt_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_prompts() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM prompts ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_prompt(prompt_id: int, name: str = None, content: str = None, description: str = None) -> bool:
    conn = get_db()
    prompt = conn.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,)).fetchone()
    if not prompt:
        conn.close()
        return False

    new_name = name if name is not None else prompt["name"]
    new_content = content if content is not None else prompt["content"]
    new_description = description if description is not None else prompt["description"]

    conn.execute("""
        UPDATE prompts
        SET name = ?, content = ?, description = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_name, new_content, new_description, prompt_id))
    conn.commit()

    version_num = conn.execute(
        "SELECT COALESCE(MAX(version), 0) + 1 as v FROM prompt_versions WHERE prompt_id = ?",
        (prompt_id,)
    ).fetchone()["v"]
    conn.execute("INSERT INTO prompt_versions (prompt_id, version, content) VALUES (?, ?, ?)",
                 (prompt_id, version_num, prompt["content"]))
    conn.commit()
    conn.close()
    return True

def delete_prompt(prompt_id: int) -> bool:
    conn = get_db()
    cursor = conn.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_prompt_versions(prompt_id: int) -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM prompt_versions WHERE prompt_id = ? ORDER BY version DESC",
        (prompt_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
