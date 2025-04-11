from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a lightweight sentence embedding model.
embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def preprocess_text(knowledge_text):
    # For example, split the knowledge base into paragraphs.
    chunks = knowledge_text.split("\n\n")
    return [chunk.strip() for chunk in chunks if chunk.strip()]

# Example knowledge base as a long string.
knowledge_base = """
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

# Preprocess the knowledge base.
chunks = preprocess_text(knowledge_base)

# Convert each chunk into an embedding.
embeddings = embedder.encode(chunks, convert_to_numpy=True)

# Create a FAISS index with L2 (Euclidean) distance.
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# A helper function for retrieval.
def retrieve_relevant_context(query, k=3):
    query_vec = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, k)
    # Concatenate the retrieved chunks.
    context = " ".join([chunks[i] for i in indices[0]])
    return context

# Example: retrieving context for a sample question.
sample_question = "What is Narrow AI?"
context_for_sample = retrieve_relevant_context(sample_question)
# print("Retrieved context:", context_for_sample)


from transformers import pipeline

# Use a more capable model, such as Flan-T5-base.
qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base", 
    tokenizer="google/flan-t5-base",
    device=0  # Set to 0 if using GPU, or -1 for CPU
)

def answer_question(question, context):
    prompt = (
        "You are a friendly assistant who loves to help people with a warm, human-like approach.\n\n"
        "Example dialogue:\n"
        "User: Hi there! Can you tell me about Narrow AI?\n"
        "Assistant: Hello! I'd be happy to explain. Narrow AI, also known as weak AI, refers to systems that "
        "are designed to perform a specific task, like image recognition or language translation. Although "
        "they excel at what they do, they lack general intelligence and cannot perform tasks outside their domain.\n\n"
        "Now, please answer the following question in a similar friendly and detailed manner:\n\n"
        f"Question: {question}\n\n"
        f"Context: {context}\n\n"
        "Answer: "
    )
    result = qa_pipeline(
        prompt,
        max_length=300,
        do_sample=True,
        temperature=0.8,
        top_p=0.9
    )
    return result[0]["generated_text"]

# Example usage:
sample_question = "What is General AI?"
print("Generated Output:", answer_question(sample_question, context_for_sample))
