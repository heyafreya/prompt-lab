from .db import get_db

def get_all_prompts() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM prompts ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_prompt(prompt_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

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

def get_all_models() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM models ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_model(name: str, provider: str) -> int:
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO models (name, provider) VALUES (?, ?)",
        (name, provider)
    )
    conn.commit()
    model_id = cursor.lastrowid
    conn.close()
    return model_id

def get_experiments_with_details() -> list[dict]:
    conn = get_db()
    rows = conn.execute("""
        SELECT
            e.id, e.input_text, e.output_text, e.latency_ms,
            e.tokens_used, e.status, e.created_at,
            p.name as prompt_name, p.content as prompt_content,
            m.name as model_name, m.provider as model_provider
        FROM experiments e
        JOIN prompts p ON e.prompt_id = p.id
        JOIN models m ON e.model_id = m.id
        ORDER BY e.created_at DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_model_stats() -> list[dict]:
    conn = get_db()
    rows = conn.execute("""
        SELECT
            m.name, m.provider,
            COUNT(e.id) as experiment_count,
            ROUND(AVG(e.latency_ms), 1) as avg_latency_ms,
            SUM(e.tokens_used) as total_tokens,
            ROUND(AVG(mt.quality_score), 2) as avg_quality
        FROM models m
        LEFT JOIN experiments e ON e.model_id = m.id
        LEFT JOIN metrics mt ON mt.experiment_id = e.id
        GROUP BY m.id
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_prompt_stats() -> list[dict]:
    conn = get_db()
    rows = conn.execute("""
        SELECT
            p.name, p.description,
            COUNT(e.id) as experiment_count,
            ROUND(AVG(e.latency_ms), 1) as avg_latency_ms
        FROM prompts p
        LEFT JOIN experiments e ON e.prompt_id = p.id
        GROUP BY p.id
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_experiment(prompt_id: int, model_id: int, input_text: str) -> int:
    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO experiments (prompt_id, model_id, input_text, status)
        VALUES (?, ?, ?, 'pending')
    """, (prompt_id, model_id, input_text))
    conn.commit()
    exp_id = cursor.lastrowid
    conn.close()
    return exp_id

def update_experiment_result(exp_id: int, output_text: str, latency_ms: float, tokens_used: int, status: str = 'completed'):
    conn = get_db()
    conn.execute("""
        UPDATE experiments
        SET output_text = ?, latency_ms = ?, tokens_used = ?, status = ?
        WHERE id = ?
    """, (output_text, latency_ms, tokens_used, status, exp_id))
    conn.commit()
    conn.close()

def get_experiment(exp_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
