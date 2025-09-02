# feedback_memory.py
import json
import os
from datetime import datetime

class FeedbackMemory:
    def __init__(self, history_file="feedback_history.json"):
        self.blog_tips = []
        self.social_tips = []
        self.history_file = history_file
        self.history = []
        self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] FeedbackMemory: Failed to save history. {e}")

    def add_feedback(self, kind, title, theme, scores, reasoning, attempt, accepted=False):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": kind,
            "title": title,
            "theme": theme,
            "scores": scores,
            "reasoning": reasoning,
            "attempt": attempt,
            "accepted": accepted
        }
        self.history.append(record)
        self._save_history()

        # reinforcement: separate successes and improvement tips
        overall = scores.get("overall", 0)
        tip = f"{reasoning} (score={overall})"
        if overall >= 0.80:
            if kind == "blog":
                self.blog_tips.append(f"✅ {tip}")
            elif kind == "social":
                self.social_tips.append(f"✅ {tip}")
        else:
            if kind == "blog":
                self.blog_tips.append(f"⚠️ {tip}")
            elif kind == "social":
                self.social_tips.append(f"⚠️ {tip}")

    def get_improvement_tips(self, kind="blog"):
        tips = self.blog_tips if kind == "blog" else self.social_tips
        return " ".join([t for t in tips if t.startswith("⚠️")][-3:])

    def get_success_patterns(self, kind="blog"):
        tips = self.blog_tips if kind == "blog" else self.social_tips
        return " ".join([t for t in tips if t.startswith("✅")][-3:])

FeedbackMemorySingleton = FeedbackMemory()
