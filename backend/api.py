import os
import re
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    return match.group(1) if match else None


def get_transcript(video_url):
    video_id = extract_video_id(video_url)

    if not video_id:
        return ""

    try:
        data = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        return " ".join([t.text for t in data])
    except:
        return ""


def create_vector_store(transcript):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    docs = splitter.create_documents([transcript])[:50]
    return FAISS.from_documents(docs, embeddings)


def chat_with_video(video_url, question):
    transcript = get_transcript(video_url)

    if not transcript:
        return "No transcript available."

    vector_store = create_vector_store(transcript)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
Answer ONLY using context. If not found, say "I don't know".

Context:
{context}

Question:
{question}
"""

    return llm.invoke(prompt).content


def summarize_video(video_url):
    transcript = get_transcript(video_url)

    if not transcript:
        return "No transcript available."

    prompt = f"""
Summarize into bullet points (max 10):

{transcript}
"""

    return llm.invoke(prompt).content
