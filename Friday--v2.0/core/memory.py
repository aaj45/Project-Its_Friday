import json
import os


class MemoryManager:
    def __init__(self, file="fridays_memory.json"):
        self.file = file
        self.data = self._load()

    def _load(self):
        """Load memory from disk."""
        if not os.path.exists(self.file):
            return {
                "facts": [],
                "dialogue": []
            }

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"Memory load error: {e}")

            return {
                "facts": [],
                "dialogue": []
            }

    def save(self):
        """Save memory to disk."""
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(
                    self.data,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as e:
            print(f"Memory save error: {e}")

    # --------------------
    # DIALOGUE MEMORY
    # --------------------

    def add_dialogue(self, role, content):
        self.data["dialogue"].append({
            "role": role,
            "content": content
        })

        # Keep last 100 messages
        self.data["dialogue"] = self.data["dialogue"][-100:]

        self.save()

    def get_dialogue(self):
        return self.data.get("dialogue", [])

    def clear_dialogue(self):
        self.data["dialogue"] = []
        self.save()

    # --------------------
    # FACT MEMORY
    # --------------------

    def add_fact(self, fact):
        fact = fact.strip()

        if not fact:
            return

        if fact not in self.data["facts"]:
            self.data["facts"].append(fact)

        # Keep last 50 facts
        self.data["facts"] = self.data["facts"][-50:]

        self.save()

    def get_facts(self):
        return self.data.get("facts", [])

    def clear_facts(self):
        self.data["facts"] = []
        self.save()

    # --------------------
    # UTILITY FUNCTIONS
    # --------------------

    def clear_all(self):
        self.data = {
            "facts": [],
            "dialogue": []
        }

        self.save()

    def memory_summary(self):
        return {
            "facts_count": len(self.data["facts"]),
            "dialogue_count": len(self.data["dialogue"])
        }