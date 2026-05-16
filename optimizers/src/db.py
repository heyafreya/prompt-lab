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

def seed_data():
    conn = get_db()

    conn.execute("INSERT OR IGNORE INTO models (name, provider) VALUES ('gpt-4', 'openai')")
    conn.execute("INSERT OR IGNORE INTO models (name, provider) VALUES ('claude-3', 'anthropic')")
    conn.execute("INSERT OR IGNORE INTO models (name, provider) VALUES ('gemini-pro', 'google')")

    conn.execute("INSERT OR IGNORE INTO prompts (name, content, description) VALUES ('summarizer', 'Summarize this: ', 'Summarizes text')")
    conn.execute("INSERT OR IGNORE INTO prompts (name, content, description) VALUES ('coder', 'Write code for: ', 'Code generation')")
    conn.execute("INSERT OR IGNORE INTO prompts (name, content, description) VALUES ('explainer', 'Explain like I''m 5: ', 'Simple explanations')")

    conn.commit()

    for p in range(1, 4):
        for m in range(1, 4):
            for i in range(2):
                conn.execute("""
                    INSERT INTO experiments (prompt_id, model_id, input_text, output_text, latency_ms, tokens_used, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'completed')
                """, (p, m, f"input {i}", f"output {i}", 100 + p*50 + m*10 + i*20, 50 + i*10))

    conn.execute("""
        INSERT INTO metrics (experiment_id, response_time_ms, token_count, cost_usd, quality_score)
        SELECT id, latency_ms, tokens_used, tokens_used * 0.0001, 0.5 + RANDOM() * 0.5
        FROM experiments
    """)

    conn.commit()
    conn.close()
    print("Seed data added!")

if __name__ == "__main__":
    init_db()
    seed_data()
    print(f"Database ready at {DB_PATH}")
