# app/llm/knowledge.py

from transformers import pipeline

class KnowledgeBaseLLM:
    def __init__(self, pdf_text: str):
        """
        Initialize the KnowledgeBaseLLM with extracted PDF text.
        It prepares the context and initializes the LLM pipeline.
        """
        self.context = self.prepare_context(pdf_text)
        # Initialize an LLM pipeline (using Flan-T5-base as an example).
        self.qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            tokenizer="google/flan-t5-base",
            device=0  # Use 0 for GPU, or set -1 for CPU.
        )

    def prepare_context(self, text: str) -> str:
        """
        Prepares or cleans the PDF text. You can enhance this function with more advanced
        preprocessing (e.g., splitting into paragraphs, removing noise, etc.)
        """
        return text.strip()

    def answer_question(self, question: str) -> str:
        """
        Generate a detailed, friendly answer for the given question using the stored context.
        """
        prompt = (
            "You are a friendly assistant who loves to help people with a warm, human-like approach.\n\n"
            "Example dialogue:\n"
            "User: Hi there! Can you tell me about Narrow AI?\n"
            "Assistant: Hello! I'd be delighted to explain. Narrow AI, also known as weak AI, "
            "refers to systems that are specifically designed to perform a single task, such as image recognition or language translation. "
            "While they can be extremely proficient at their tasks, they lack the general problem-solving abilities of human intelligence.\n\n"
            "Now, please answer the following question in a similar friendly and detailed manner:\n\n"
            f"Question: {question}\n\n"
            f"Context: {self.context}\n\n"
            "Answer: "
        )
        result = self.qa_pipeline(
            prompt,
            max_length=300,
            do_sample=True,
            temperature=0.8,
            top_p=0.9
        )
        return result[0]["generated_text"]
