import os

from chatbot import ChatBot
from flask import Flask, request, jsonify


##로컬 엘라스틱 사용시
class FlaskApp:
    def __init__(self, api_key):
        self.app = Flask(__name__)
        self.chatbot = ChatBot(api_key)

        @self.app.route('/botresponse', methods=['POST'])
        def send_message():
            try:
                data = request.get_json()
                room_id = data['roomId']
                user_id = data['userId']
                question = data['message']

                response = self.chatbot.run_chatbot(room_id, user_id, question)
                return jsonify({"bot_response": response, "userId": user_id})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    api_key = os.getenv("OPENAI_API_KEY")
    flask_app = FlaskApp(api_key)
    flask_app.run()


## elasticsearch를 클라우드 버전으로 사용시
# class FlaskApp:
#     def __init__(self, endpoint, api_key):
#         self.app = Flask(__name__)
#         self.chatbot = ChatBot(endpoint, api_key)

#         @self.app.route('/botresponse', methods=['POST'])
#         def send_message():
#             try:
#                 data = request.get_json()
#                 room_id = data['roomId']
#                 user_id = data['userId']
#                 question = data['message']

#                 response = self.chatbot.run_chatbot(room_id, user_id, question)
#                 return jsonify({"bot_response": response, "userId": user_id})
#             except Exception as e:
#                 return jsonify({"error": str(e)}), 500

#     def run(self):
#         self.app.run(host='0.0.0.0', port=5000)


# if __name__ == '__main__':
#     endpoint = os.getenv("ENDPOINT")
#     api_key = os.getenv("OPENAI_API_KEY")
#     flask_app = FlaskApp(endpoint, api_key)
#     flask_app.run()
