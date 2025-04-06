import copy
import random
from typing import List, Dict
from src.knowledge import document_retrieval
from src.instruct import *
from openai import OpenAI
import json

# base_url = os.environ['BASE_URL']
api_key = [
    'sk-LyjNjNUGmBs0xTftABbAq9m0WDDCQPKuLM6y3Y4tVHQMQCQK'
]

def get_from_openai(model: str,
                    messages: List[Dict],
                    stop: List[str],
                    max_len: int = 512,
                    temp: float = 0.0,
                    n: int = 1, ):
    cnt = 0
    while cnt < 10:
        # try to request openAI for multiple times in case of poor network
        try:
            client = OpenAI(
                api_key=api_key[random.randint(0, 10000) % len(api_key)],
                base_url="https://api.chatanywhere.tech/v1"
            )
            kwargs = {
                "model": model,
                'max_tokens': max_len,
                "temperature": temp,
                "n": n,
                'stop': stop,
                "messages": messages
            }
            response = client.chat.completions.create(**kwargs)

            response = response.choices[0].message.content if n == 1 else [choice.message.content for choice in response.choices]
            return response
        except:
            print(f'request {model} again ... {cnt}')
            cnt += 1
    return 'no response from openai model...'


class GenGround:
    def __init__(self,
            model: str='gpt-3.5-turbo-0613',
            retrieval: str='oracle',
            n_docs: int=9,
            batch_doc_size: int=3,
            corpus: str = 'wiki'
    ):
        # print(f'the foundation model is {model}')
        self.model = model
        self.retrieval = retrieval
        self.corpus = corpus
        self.n_docs = n_docs
        self.batch_doc_size = batch_doc_size


    @property
    def name(self):
        return 'GenGround'

    def grounding(self, question, answer, docs, batch_size=3):
        def _batch_grounding(model_name, q, a, docs):
            # craft this prompt based on the openAI prompt guidance: https://platform.openai.com/docs/guides/prompt-engineering/six-strategies-for-getting-better-results
            prompt = """Please help me to revise the factual error in my answer to a question by referring the relevant evidence"""
            input_docs = """You are provided with {n} documents from Wikipedia; each document is identified with a numeric identifier, e.g., [1] and [2]. You should read these document carefully.         
Starting below, please cite relevant evidence from the documents to check my answer to a question and revise my answer into a correct one if it is wrong. You should first give the evidence your cite and then give the answer; If you find no evidence can be used to check my answer, please retain my answer. The answer is a short span.
Here are some examples you should follow to formate your output.

Here is a question: What is the favorite color of the author? And my answer is: Blue.
Your output: No relevant evidence found in the documents. I will retain the original answer
Answer: Blue.

Here is a question: Who discovered penicillin? And my answer is: Marie Curie.
Citation: [1] indicates that "Fleming discovered penicillin in 1928 when he noticed that a mold called Penicillium notatum killed bacteria in his Petri dishes"
Answer: Alexander Fleming"""
            receive_doc = "Sure, please send me your question and answer. I will check whether the answer is correct based on your documents."

            user = """Document:
{docs}

Here is a question: {question}? And my answer is: {answer}
Citation: """

            _docs = '\n'.join([f'[{i}] {d}' for i, d in enumerate(docs, 1)])
            messages = [
                {"role": "system", 'content': prompt},
                {"role": "user", 'content': input_docs.format(n=len(docs))},
                {"role": "assistant", 'content': receive_doc},
                {"role": "user", 'content': user.format(question=q, answer=a, docs=_docs)},
            ]
            response = get_from_openai(model=model_name, messages=messages,temp=0.5, stop=[])
            try:
                citation, _a = response.split('Answer:')
            except:
                citation = response.split('\n')[0].strip()
                messages[-1]['content'] += f'{citation}\nAnswer: '
                _a = get_from_openai(model=model_name, messages=messages,temp=0.5, stop=[])
            return citation, _a

        tmp = copy.deepcopy(docs)
        # queue to iteratively append useful evidence and filter noise doc
        for i in range(0, len(docs), batch_size):
            citation, _answer = _batch_grounding(self.model, question, answer,tmp[i:i+batch_size])
            if any([f"[{i}]" in citation for i in range(batch_size)]):
                return _answer
        return answer

    def noramlize(self, s):
        eee = ['[1]', '[2]', '[3]', '[4]', '[5]', '()', '\n', '\t', '[', ']', 'FINISH', 'finish', 'Finish']
        for e in eee:
            s = s.replace(e, '')
        return s.strip()

    def generate(self, line, corpus='psgs'):
        print(line['query'])
        if line['dataset'] == 'boolqa':
            prompt = BOOL_GENERATION_USER.format(icl_example=icl_example[line['dataset']], query=line['query'])
        else:
            prompt = GENERATION_USER.format(icl_example=icl_example[line['dataset']], query=line['query'])

        for i in range(1, 8):
            # question -> sub-question, immediate answer
            response = get_from_openai(
                model=self.model,
                messages=[{'role': 'system', 'content': GENERATION_SYSTEM},
                          {"role": "user", "content": prompt + f'<Thought> '}],
                stop=['<Thought>'],
                temp=0.5
            )
            try:
                # parse the LLM response
                q, answer = [line.strip() for line in response.split('<Answer>')]
            except:
                # post-processing if the response format is unaligned （See ReAct https://github.com/ysymyth/ReAct/blob/master/hotpotqa.ipynb)
                q = response.strip().split('\n')[0]
                answer = get_from_openai(
                    model=self.model,
                    messages=[{'role': 'system', 'content': GENERATION_SYSTEM},
                              {"role": "user", "content": prompt + f'<Thought> {q}\n<Answer>'}],
                    stop=['\n'],
                    temp=0,
                )
                answer = answer.strip().replace('\n', '')

            #  `Finish` is a pre-defined signal in prompt to indicate finish the question
            if 'finish' in answer.lower():
                answer = self.noramlize(answer)
                prompt += f"<Thought> {q}\n<Answer> {answer}\n"
                return prompt, answer

            q = self.noramlize(q)
            answer = self.noramlize(answer)
            print(f"<Thought> {q} ({answer})")

            # retrieve document for knowledge augmentation
            # raw_doc = Knowledge.get_knowledge(line, mode=self.retrieval, corpus=self.corpus, query=q, k=self.n_docs)
            raw_doc = document_retrieval(query=q, k=9)

            # sub-question, immediate answer -> calibrated answer
            _answer = self.grounding(question=q, answer=answer, docs=raw_doc, batch_size=self.batch_doc_size)
            _answer = self.noramlize(_answer)
            prompt += f"<Thought> {q}\n<Answer> {_answer}\n"
            print(f"<Answer> {_answer}")
        return 'NO ANSWER'


