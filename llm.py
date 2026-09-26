from utils.thinking import ThinkingIndicator
import ollama


class LLM:
    def __init__(self, memory, emotion):
        self.memory = memory
        self.emotion = emotion
        self.thinker = ThinkingIndicator()

        # Load stored facts
        facts = self.memory.get_facts()

        system_prompt = (
            "You are Friday, a calm, intelligent, and helpful AI assistant.\n\n"
            "Known facts about the user:\n"
        )

        if facts:
            for fact in facts:
                system_prompt += f"- {fact}\n"
        else:
            system_prompt += "- No known facts yet.\n"

        self.conversation = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Load previous dialogue history
        self.conversation.extend(
            self.memory.get_dialogue()
        )

    def ask(self, prompt):
        self.emotion.update(prompt)

        # Store important user facts
        self._extract_fact(prompt)

        self.conversation.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # Keep context from growing too large
        self.conversation = (
            self.conversation[:1] +
            self.conversation[-50:]
        )

        self.thinker.start()

        try:
            response = ollama.chat(
                model="llama3",
                messages=self.conversation
            )

            reply = response["message"]["content"]

            self.conversation.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            self.memory.add_dialogue(
                "user",
                prompt
            )

            self.memory.add_dialogue(
                "assistant",
                reply
            )

            return reply

        except Exception as e:
            print(f"⚠️ LLM error: {e}")
            return "Sorry, something went wrong."

        finally:
            self.thinker.stop()

    def _extract_fact(self, text):
        """
        Extract simple user facts and save them.
        """

        text_lower = text.lower()

        fact_patterns = [
            "my name is",
            "i am",
            "i'm",
            "my favourite",
            "my favorite",
            "i live in",
            "i work at",
            "i work for",
            "my birthday is",
            "my wife is",
            "my husband is",
            "my son is",
            "my daughter is"
        ]

        if any(pattern in text_lower for pattern in fact_patterns):
            self.memory.add_fact(text)