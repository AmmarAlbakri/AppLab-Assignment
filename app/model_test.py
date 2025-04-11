from llm.model import KnowledgeBaseLLM  # Import the class from the separate file

text = """
Introduction to Artificial Intelligence (AI):
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines designed to think like humans.

Types of AI:
There are three main types of AI: Narrow AI, General AI, and Superintelligent AI.
- Narrow AI: specialized on a single task.
- General AI: capable of performing any intellectual task.
- Superintelligent AI: exceeds human intelligence in all domains.

Machine Learning (ML):
Machine learning is a subset of AI which uses algorithms to learn from data.

Deep Learning (DL):
Deep learning is a subset of ML that utilizes neural networks to learn from vast amounts of data.

AI Applications:
AI finds applications in healthcare, finance, automotive, and more.
"""
llm_instance = KnowledgeBaseLLM(text)
answer = llm_instance.answer_question("In which industries is AI applied?")
print(answer)