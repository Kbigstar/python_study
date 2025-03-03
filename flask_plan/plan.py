from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langchain.chains import LLMChain
import json
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
class JSONOutputParser(BaseOutputParser):
    """Parser that converts a JSON string output into a Python dictionary or list."""
    def parse(self, text: str):
        print('before:', text)
        return json.loads(text)


class PlanGPT():

    def __init__(self):
        self.api_key="" # Chat GPT API_KEY
        self.chat_model = ChatOpenAI(openai_api_key=self.api_key)
        self.user_plan = []
        self.template = """
                        당신은 2024년에 활동하는 일정 추천 AI 비서입니다. 
                        사용자로부터 받은 일정 데이터는 JSON 형식으로 되어 있으며, 
                        사용자의 기존 일정을 고려하여 그 시간을 제외한 나머지 시간에 할 수 있는 
                        활동을 추천하는 역할을 합니다. 
                        
                        사용자의 일정은 시작 시각(calStartdt)과 종료 시각(calEnddt)으로 정의됩니다. 
                        당신의 임무는 사용자의 기존 일정 외의 시간을 활용하여 3가지 다른 활동을 제안하는 것입니다.
                        데이터는 {user_plan} 이거야
                        
                        조건1:유저의 기존 스케줄은 언급 하지 않아도됨.
                        조건2:응답은 json 데이터 형태로 다양하게 3개정도 추천
                        예를 들어 변수는 activity의 배열 형태로 
                        - calTitle:요가 
                        - calStartdt:2024-03-14T17:00  
                        - calEnddt:2024-03-14T19:00
                        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.template)
        self.human_template = "{text}"
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt, self.human_message_prompt])

        self.chain = LLMChain(
            llm=ChatOpenAI(api_key=self.api_key),
            prompt=self.chat_prompt,
            output_parser=JSONOutputParser()
        )

    def sendGpt(self, plan, msg="여가 계획을 계획해줘"):
        result = self.chain.run(text=msg, user_plan=json.dumps(plan))
        return result

if __name__ == '__main__':
    gpt = PlanGPT()
    user_plan = [{
        "calAllday": "false",
        "calBgcolor": "#000000",
        "calNo": 202,
        "calStartdt": "2024-03-14T09:00",
        "calEnddt": "2024-03-14T16:00",
        "calTextcolor": "#ffffff",
        "calTitle": "개인프로젝트 준비",
        "delYn": "N",
        "memId": "kbs",
    }]
    print(gpt.sendGpt("5일치 계획 만들고 싶어", user_plan))