import os
from dotenv import load_dotenv

from openai import OpenAI
from elasticsearch import Elasticsearch
#from langchain_openai import OpenAIEmbeddings

class DocumentSearcher:
    def __init__(self, api_key):
        # .env 파일에서 환경 변수 로드
        load_dotenv()
        #openai api key
        self.openAIclient = OpenAI() 
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.openAIclient.api_key = self.api_key
        #elasticsearch password
        self.es_pw = os.getenv('ES_PW')
        
        self.client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme':'http'}], http_auth=('elastic', self.es_pw) )
        #self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
 
        
        
    # 텍스트 임베딩 함수
    def get_embedding(self, text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return self.openAIclient.embeddings.create(input = [text], model=model).data[0].embedding
    
    #gpt를 사용한 의도분류 함수
    def classify_intent(self, question):
        response = self.openAIclient.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "당신은 사용자의 질문 의도를 잘 판단하는 전문가입니다. 사용자가 청년 정책 관련 정보를 원하는지, 특정 용어 설명을 원하는지 구분해 주세요. 만약 청년 정책 정보를 원한다면 'policy', 용어 설명을 원한다면 'word'라고만 반환하세요. 만약 둘다 해당 안 될 시 'policy'라고 반환하세요"},
                      {"role": "user", "content": question}]
        )
        print(f'의도 분류: {response.choices[0].message.content}')
        return response.choices[0].message.content

    #
    def search_similar_documents(self, question):
        #question_embedding = self.embeddings.embed_documents([question])[0]
        question_embedding = self.get_embedding(question)
        INTENDED_INDEX = self.classify_intent(question)
        response = self.client.search(
            index=INTENDED_INDEX,
            body={
                "size": 3,
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                            "params": {"query_vector": question_embedding}
                        }
                    }
                }
            }
        )
        print([f"#{i+1} {hit['_source']['text']}" for i, hit in enumerate(response['hits']['hits'])])
        return [f"#{i+1} {hit['_source']['text']}" for i, hit in enumerate(response['hits']['hits'])]