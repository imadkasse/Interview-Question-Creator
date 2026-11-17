from langchain_community.vectorstores import FAISS
def vec_db(docs_answer_gen , embedding):
    vector_store = FAISS.from_documents(docs_answer_gen , embedding=embedding)
    return vector_store