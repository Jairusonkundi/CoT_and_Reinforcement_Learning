# feedback.py
import json
import os
from datetime import datetime

# Files used to persist feedback & rewards
FEEDBACK_LOG_FILE = "feedback.log"
SCORES_HISTORY_FILE = "feedback_history.json"
REWARD_STORE_FILE = "reward_store.json"

# ----------------- Utility Functions -----------------
def _load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def _save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def _append_log(text):
    try:
        with open(FEEDBACK_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - {text}\n")
    except Exception:
        pass

# ----------------- Reinforcement Learning Helpers -----------------
def _get_theme_history(theme, content_type):
    history = _load_json(SCORES_HISTORY_FILE, [])
    return [entry for entry in history if entry["theme"] == theme and entry["type"] == content_type]

def _score_length(content: str):
    word_count = len(content.split())
    if word_count < 100:
        return 0.5
    elif word_count < 500:
        return 0.7
    elif word_count < 1500:
        return 0.85
    else:
        return 0.95

def _score_clarity(content: str):
    sentences = content.split(".")
    avg_len = sum(len(s.split()) for s in sentences if s.strip()) / max(len(sentences), 1)
    if avg_len < 12:
        return 0.9
    elif avg_len < 20:
        return 0.8
    else:
        return 0.65

def _score_engagement(content: str):
    engagement_features = sum([
        "?" in content,
        "!" in content,
        "call us" in content.lower(),
        "learn more" in content.lower(),
    ])
    return min(0.6 + 0.1 * engagement_features, 0.95)

def _score_structure(content: str):
    paragraphs = content.count("\n\n")
    headings = sum(1 for line in content.split("\n") if line.strip().startswith("#") or line.strip().endswith(":"))
    bullets = content.count("- ") + content.count("* ")
    return min(0.6 + 0.1 * (paragraphs + headings + bullets), 0.95)

def _reinforce_with_history(theme, content_type, scores):
    history = _get_theme_history(theme, content_type)
    if history:
        best = max(history, key=lambda x: x["scores"]["overall"])
        for key in scores:
            scores[key] = min(scores[key] + 0.05, 1.0)
    return scores

def _compute_reinforced_scores(theme, content, content_type="blog"):
    scores = {
        "length": _score_length(content),
        "clarity": _score_clarity(content),
        "engagement": _score_engagement(content),
        "structure": _score_structure(content),
    }
    scores = _reinforce_with_history(theme, content_type, scores)
    scores["overall"] = round(sum(scores.values()) / len(scores), 2)
    return {k: round(v, 2) for k, v in scores.items()}

def _compute_reinforced_social_scores(theme, title, content):
    scores = {
        "length": _score_length(content),
        "clarity": _score_clarity(content),
        "engagement": _score_engagement(content),
        "relevance": 0.8 if theme.lower() in (title + content).lower() else 0.65,
    }
    scores = _reinforce_with_history(theme, "social", scores)
    scores["overall"] = round(sum(scores.values()) / len(scores), 2)
    return {k: round(v, 2) for k, v in scores.items()}

# ----------------- Public Evaluation -----------------
def evaluate_blog_ai(title, content, theme=None):
    scores = _compute_reinforced_scores(theme, content, "blog")
    reasoning = "Evaluated based on word count, clarity (sentence length), engagement signals, and structure."
    return scores, reasoning

def evaluate_social_ai(title, post, theme=None):
    scores = _compute_reinforced_social_scores(theme, title, post)
    reasoning = "Evaluated based on word count, clarity, engagement features, and relevance to theme."
    return scores, reasoning

# ----------------- Reward / Record -----------------
def compute_reward_from_scores(scores, threshold=0.8):
    return round(max(scores.get("overall", 0) - threshold, 0.0), 3)

def update_reward_store(theme, content_type, reward):
    store = _load_json(REWARD_STORE_FILE, {"themes": {}, "by_type": {}})
    
    # Update per-theme rewards
    t = store.get("themes", {}).get(theme, {"total_reward": 0.0, "count": 0})
    t["total_reward"] = round(t.get("total_reward", 0.0) + reward, 3)
    t["count"] = t.get("count", 0) + 1
    t["avg"] = round(t["total_reward"] / t["count"], 3)
    store.setdefault("themes", {})[theme] = t

    # Update per-content-type rewards
    bt = store.get("by_type", {}).get(content_type, {"total": 0.0, "count": 0})
    bt["total"] = round(bt.get("total", 0.0) + reward, 3)
    bt["count"] = bt.get("count", 0) + 1
    bt["avg"] = round(bt["total"] / bt["count"], 3)
    store.setdefault("by_type", {})[content_type] = bt

    _save_json(REWARD_STORE_FILE, store)
    return t["avg"]

def record_feedback(content_type, title, theme, scores, reasoning, attempt=1, accepted=True, threshold=0.8):
    history = _load_json(SCORES_HISTORY_FILE, [])
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": content_type,
        "title": title,
        "theme": theme,
        "scores": scores,
        "reasoning": reasoning,
        "attempt": attempt,
        "accepted": bool(accepted)
    }
    history.append(entry)
    _save_json(SCORES_HISTORY_FILE, history)

    reward = compute_reward_from_scores(scores, threshold)
    theme_avg = update_reward_store(theme, content_type, reward)

    _append_log(f"{content_type.upper()} | '{title}' | theme='{theme}' | attempt={attempt} "
                f"| overall={scores.get('overall')} | reward={reward} | avg={theme_avg}")
    return reward, theme_avg
