from .document_searcher import DocumentSearcher

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder


class ChatBot:
    def __init__(self, endpoint, api_key):
        #self.history_manager = ChatHistoryManager(endpoint, api_key)
        self.document_searcher = DocumentSearcher(api_key)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ('system', "{context}을 잘 요약해서 사용자 질문에 답을 생성해줘. 관련성이 낮은 질문은 모른다고 대답해."),
                MessagesPlaceholder(variable_name='history'),
                ('user', '{question}'),
            ]
        )
        # self.prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ('system', "당신은 청년 정책 전문가입니다. 외부 지식 없이 사용자의 질문에 대해 제공된 context 정보만 사용해 답변하세요. context는 #1, #2, #3으로 구분되어 있습니다. 필요한 한 가지 문맥 정보만을 참고하여 사용자에게 예상답처럼 답변을 제공해 주세요."),
        #         ('context', '{context}'),
        #         MessagesPlaceholder(variable_name='history'),
        #         ('user', '{question}'),
        #     ]
        # )
        self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        self.runnable = self.prompt | self.llm

        self.with_message_history = RunnableWithMessageHistory(
            self.runnable,
            self.history_manager.get_chat_history,
            input_messages_key='question',
            history_messages_key='history',
            history_factory_config=[
                ConfigurableFieldSpec(id='chat_id', annotation=str),
                ConfigurableFieldSpec(id='user_id', annotation=str)
            ],
        )

    def run_chatbot(self, chat_id, user_id, question):
        context = self.document_searcher.search_similar_documents(question)
        inputs = {
            "question": question,
            "context": context
        }
        response = self.with_message_history.invoke(
            inputs,
            config={"configurable": {"chat_id": chat_id, "user_id": user_id}}
        )

        history = self.history_manager.get_chat_history(chat_id, user_id)
        history.add_message(HumanMessage(content=question))
        self.history_manager.save_chat_history(chat_id, user_id, history)

        return response.content




## 원본
# class ChatBot:
#     def __init__(self, endpoint, api_key):
#         self.history_manager = ChatHistoryManager(endpoint, api_key)
#         self.document_searcher = DocumentSearcher(endpoint, api_key)
#         self.prompt = ChatPromptTemplate.from_messages(
#             [
#                 ('system', "{context}을 잘 요약해서 사용자 질문에 답을 생성해줘. 관련성이 낮은 질문은 모른다고 대답해."),
#                 MessagesPlaceholder(variable_name='history'),
#                 ('user', '{question}'),
#             ]
#         )
#         # self.prompt = ChatPromptTemplate.from_messages(
#         #     [
#         #         ('system', "당신은 청년 정책 전문가입니다. 외부 지식 없이 사용자의 질문에 대해 제공된 context 정보만 사용해 답변하세요. context는 #1, #2, #3으로 구분되어 있습니다. 필요한 한 가지 문맥 정보만을 참고하여 사용자에게 예상답처럼 답변을 제공해 주세요."),
#         #         ('context', '{context}'),
#         #         MessagesPlaceholder(variable_name='history'),
#         #         ('user', '{question}'),
#         #     ]
#         # )
#         self.llm = ChatOpenAI(model="gpt-3.5-turbo")
#         self.runnable = self.prompt | self.llm

#         self.with_message_history = RunnableWithMessageHistory(
#             self.runnable,
#             self.history_manager.get_chat_history,
#             input_messages_key='question',
#             history_messages_key='history',
#             history_factory_config=[
#                 ConfigurableFieldSpec(id='chat_id', annotation=str),
#                 ConfigurableFieldSpec(id='user_id', annotation=str)
#             ],
#         )

#     def run_chatbot(self, chat_id, user_id, question):
#         context = self.document_searcher.search_similar_documents(question)
#         inputs = {
#             "question": question,
#             "context": context
#         }
#         response = self.with_message_history.invoke(
#             inputs,
#             config={"configurable": {"chat_id": chat_id, "user_id": user_id}}
#         )

#         history = self.history_manager.get_chat_history(chat_id, user_id)
#         history.add_message(HumanMessage(content=question))
#         self.history_manager.save_chat_history(chat_id, user_id, history)

#         return response.content