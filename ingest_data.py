from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from prepare import PINECONE_ENVIRONMENT, PINECONE_API_KEY, PINECONE_INDEX_NAME, CHATGLM_KEY
import pinecone
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
import zhipuai

filePath = 'docs'
zhipuai.api_key = "a333b62b0b117025f9c6f349b462436a.ZbNY1lGk2Pkvf4hG"



def initPinecone():
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        return pinecone
    except Exception:
        print(Exception)


def ingest():
    pineconeStorage = initPinecone()
    directoryLoader = DirectoryLoader('docs', glob='*.pdf', loader_cls=PyPDFLoader)
    rawDocs = directoryLoader.load()
    print(len(rawDocs))
    textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = textSplitter.split_documents(rawDocs)
    content_list = [chunk.page_content for chunk in docs]
    embedding_list = []
    for content in content_list:
        response = zhipuai.model_api.invoke(
            model="text_embedding",
            prompt=content
        )
        embedding_list.append(response['data']['embedding'])
        print(len(embedding_list))
    tuple_list = []
    index = pineconeStorage.Index(PINECONE_INDEX_NAME)
    print(len(embedding_list[0]))
    print(docs[0])
    for i in range(len(embedding_list)):
        metadata = {
            'text': docs[i].page_content,
            'page': docs[i].metadata['page'],
            'source': docs[i].metadata['source']
        }
        d = {
            'id': 'vec' + str(i),
            'values': embedding_list[i],
            'metadata': metadata
        }
        tuple_list.append(d)
    index.upsert(tuple_list)
    return index




if __name__ == '__main__':
    ingest()