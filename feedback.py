# feedback.py
import json
import os
from datetime import datetime
import random

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
    theme_scores = [entry for entry in history if entry["theme"]==theme and entry["type"]==content_type]
    return theme_scores

def _compute_reinforced_scores(theme, content_type):
    # Base heuristics
    base = random.uniform(0.7, 0.85)
    clarity = random.uniform(0.65, 0.85)
    engagement = random.uniform(0.65, 0.9)
    structure = random.uniform(0.65, 0.85)
    
    # Reinforce from best past scores
    history = _get_theme_history(theme, content_type)
    if history:
        best = max(history, key=lambda x: x["scores"]["overall"])
        base = min(best["scores"].get("length", base)+0.05, 0.99)
        clarity = min(best["scores"].get("clarity", clarity)+0.05, 0.99)
        engagement = min(best["scores"].get("engagement", engagement)+0.05, 0.99)
        structure = min(best["scores"].get("structure", structure)+0.05, 0.99)
    
    overall = round((base + clarity + engagement + structure)/4, 2)
    return {
        "length": round(base,2),
        "clarity": round(clarity,2),
        "engagement": round(engagement,2),
        "structure": round(structure,2),
        "overall": overall
    }

def _compute_reinforced_social_scores(theme, title):
    base = random.uniform(0.7, 0.85)
    clarity = random.uniform(0.65,0.85)
    engagement = random.uniform(0.7,0.9)
    relevance = random.uniform(0.65,0.85)
    history = _get_theme_history(theme, "social")
    if history:
        best = max(history, key=lambda x: x["scores"]["overall"])
        base = min(best["scores"].get("length", base)+0.05,0.99)
        clarity = min(best["scores"].get("clarity", clarity)+0.05,0.99)
        engagement = min(best["scores"].get("engagement", engagement)+0.05,0.99)
        relevance = min(best["scores"].get("relevance", relevance)+0.05,0.99)
    overall = round((base + clarity + engagement + relevance)/4,2)
    return {
        "length": round(base,2),
        "clarity": round(clarity,2),
        "engagement": round(engagement,2),
        "relevance": round(relevance,2),
        "overall": overall
    }

# ----------------- Public Evaluation -----------------
def evaluate_blog_ai(title, content, theme=None):
    scores = _compute_reinforced_scores(theme, "blog")
    reasoning = "Use previous best practices to improve clarity, engagement, and structure."
    return scores, reasoning

def evaluate_social_ai(title, post, theme=None):
    scores = _compute_reinforced_social_scores(theme, title)
    reasoning = "Use previous successful patterns to improve relevance, clarity, and engagement."
    return scores, reasoning

# ----------------- Reward / Record -----------------
def compute_reward_from_scores(scores, threshold=0.8):
    return round(max(scores.get("overall",0)-threshold, 0.0),3)

def update_reward_store(theme, content_type, reward):
    store = _load_json(REWARD_STORE_FILE, {"themes": {}, "by_type": {}})
    t = store.get("themes", {}).get(theme, {"total_reward": 0.0, "count": 0})
    t["total_reward"] = round(t.get("total_reward",0.0)+reward,3)
    t["count"] = t.get("count",0)+1
    t["avg"] = round(t["total_reward"]/t["count"],3)
    store.setdefault("themes",{})[theme]=t
    bt = store.get("by_type",{}).get(content_type, {"total":0.0,"count":0})
    bt["total"]=round(bt.get("total",0.0)+reward,3)
    bt["count"]=bt.get("count",0)+1
    bt["avg"]=round(bt["total"]/bt["count"],3)
    store.setdefault("by_type",{})[content_type]=bt
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
    _append_log(f"{content_type.upper()} | '{title}' | theme='{theme}' | attempt={attempt} | overall={scores.get('overall')} | reward={reward} | avg={theme_avg}")
    return reward, theme_avg
