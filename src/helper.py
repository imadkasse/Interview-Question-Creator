import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import TokenTextSplitter
from langchain_community.docstore.document import Document
from langchain_classic.chains import load_summarize_chain
from langchain_core.prompts import PromptTemplate , ChatPromptTemplate
from src.models import embeddings , llm
from src.vec_db import vec_db
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)
from src.prompt import chain_prompt,prompt_template ,refine_template





def file_procces(path):
    # load the doc
    pdf = PyPDFLoader(path)
    docs = pdf.load()
    
    question_gen = ''
    for page in docs: 
        question_gen+= page.page_content
    
    question_gen    
    chunks_question_gen = text_splitter(question_gen)
    docs_question_gen = convert_to_doc(chunks_question_gen)
    chunks_answer_gen = text_splitter(question_gen)
    docs_answer_gen = convert_to_doc(chunks_answer_gen)
    return docs_question_gen ,  docs_answer_gen

def text_splitter(question_gen):
    splitter_text_gen = TokenTextSplitter(chunk_size=10000, chunk_overlap=200)
    chunks_question_gen = splitter_text_gen.split_text(question_gen)
    return chunks_question_gen

def convert_to_doc(chunks_question_gen):
    docs_question_gen =[Document(page_content= chunk) for chunk in chunks_question_gen]
    return docs_question_gen    
    

def question_generator(prompt_template,refine_template,docs_question_gen):
    prompt_ques = PromptTemplate(template=prompt_template , input_variables=['text'])
    refine_prompt_ques = PromptTemplate(template=refine_template , input_variables=['existing_answer' , 'text'])
    ques_gen_chain = load_summarize_chain(llm = llm, 
                                          chain_type = "refine", 
                                          verbose = True, 
                                          question_prompt=prompt_ques, 
                                          refine_prompt=refine_prompt_ques
                                          )
    question = ques_gen_chain.invoke(docs_question_gen)
    
    
    return question['output_text']

def question_formater(question):
    ques_list = str(question).split('?')
    return ques_list[:10]   
def chain(file_path):
    # 
    print('file proccessing ...')
    docs_question_gen ,  docs_answer_gen  = file_procces(file_path)
    print('question generation ...')
    question = question_generator(prompt_template,refine_template,docs_question_gen )
    print('question fromater ...')
    ques_list = question_formater(question)
    print('vector db init ...')
    vector_store = vec_db(docs_answer_gen , embedding=embeddings)
    
    prompt = ChatPromptTemplate.from_messages([
    (
        "system",chain_prompt
        
    ),
    ("human", "{input}")
    ])
    question_answer_chain = create_stuff_documents_chain(
    llm,
    prompt
    )
    retrieval_chain = create_retrieval_chain(
    vector_store.as_retriever(),
    question_answer_chain
    )
    # response = retrieval_chain.invoke({
    #     "input": my_question
    # })

    # answer = response["answer"]

    # # Display
    # print(f"Question: {question}")
    # print(f"Answer: {answer}")
    # print("-" * 60)
    return retrieval_chain ,ques_list

# def answer_save(ques_list,retrieval_chain):
#     # Answer each question and save to a file
#     print('quest_list',ques_list)
#     for question in ques_list:
#         print("Question: ", question)
#         res = retrieval_chain.invoke({
#             "input": question
#         })
#         answer =res['answer']
#         print("Answer: ", answer)
#         print("--------------------------------------------------\\n\\n")
#         # Save answer to file
#         with open("answers.txt", "a") as f:
#             f.write("Question: " + question + "\\n")
#             f.write("Answer: " + answer + "\\n")
#             f.write("--------------------------------------------------\\n\\n")
            
# def main():
#     retrieval_chain , ques_list= chain()
#     answer_save(ques_list,retrieval_chain)
#     print("DONE")

# main()    
                