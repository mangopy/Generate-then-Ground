import copy
import random
from typing import List, Dict
from src.knowledge import Knowledge
from src.instruct import *
from utilze.metrics import f1_score, single_f1_score
from openai import OpenAI
import json

# base_url = os.environ['BASE_URL']
api_key = [
    'sk-ip2g65aOcppvjPBB7UDGVcciaa8jwd8yxUYHlJZOORqIHpV7'
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
        print(f'the foundation model is {model}')
        self.model = model
        self.retrieval = retrieval
        self.corpus = corpus
        self.n_docs = n_docs
        self.batch_doc_size = batch_doc_size


    @property
    def name(self):
        return 'GenGround'

    def grounding(self, q, answer, docs, batch=3):

        def _revise(model_name, q, answer, batch_doc):
            prompt = f"""You will be provided with {len(batch_doc)} documents delimited by triple quotes and a question.
Your task is to edit the candidate answer using only the provided document and to cite the passage(s) of used to edit the candidate answer.
Your answers need to be short and precise (less than 20 words). Do not introduce information that is not relevant to the question."""

            k = '\n'.join(batch_doc)

            user = """“”"{knowledge}“”"
Question: {q}
Candidate Answer: {ans}
Your output should be JSON format: {{"answer": "<the edited answer>","citation":"<cite the passage used to edit the candidate answer>"}}""".format(knowledge=k, q=q, ans=answer)

            for i in range(0, 3):
                response = get_from_openai(
                    model=model_name,
                    messages=[{"role": "system", 'content': prompt},
                              {"role": "user", 'content': user}],
                    temp=0,
                    stop=[]
                )
                try:
                    _answer = json.loads(response)['answer']
                    return _answer
                except:
                    print('json mode parse error...')

            return answer

        def _batch_grounding(model_name, q, batch_doc):
            # craft this prompt based on the openAI prompt guidance: https://platform.openai.com/docs/guides/prompt-engineering/six-strategies-for-getting-better-results
            prompt = """You will be provided with {n} documents delimited by triple quotes and a question.
Your task is to answer the question using only the provided document and to cite the passage(s) of the document used to answer the question.
Please be careful:
1. If the document does not contain the information needed to answer this question then simply write `Insufficient information`.
2. If an answer to the question is provided, it must be annotated with a citation. Use the following format to cite relevant passages ({{"citation": …}}).""".format(n=len(batch_doc))
            user = """“”"{doc}“”"\n\nQuestion: {question}""".format(doc='\n'.join(batch_doc), question=q)

            for i in range(0, 3):
                answer = get_from_openai(
                    model=model_name,
                    messages=[{"role": "system", 'content': prompt}, {"role": "user", 'content': user}],
                    stop=[],
                    temp=0,
                )
                try:
                    assert "citation" in answer or "not mentioned" in answer.lower() or 'not contain'
                    if "citation" in answer:
                        idx = answer.index("citation") + len("citation")
                        evidence = answer[idx:].replace('"', '').replace("({", '').replace("})", '').replace(":", '').strip()
                        score = single_f1_score(evidence, batch_doc)
                        return [answer[:idx]], [batch_doc[score.index(max(score))]]
                except:
                    print('citation grounding format error...')

             # "insufficient information" in answer.lower():
            return [], []

        tmp = copy.deepcopy(docs)

        # queue to iteratively append useful evidence and filter noise doc
        while len(tmp) > batch:
            _, doc = _batch_grounding(self.model, q, batch_doc=tmp[:batch])
            # discard the early stopping to find more reliable knowledge
            # if len(doc)!=0:
            #     tmp = doc
            #     break
            tmp = tmp[batch:] + doc

        if len(tmp)==0:
            return answer
        _answer = _revise(self.model, q, answer, tmp)
        return _answer

    def noramlize(self, s):
        eee = ['[1]', '[2]', '[3]', '[4]', '[5]', '()', '\n', '\t', '[', ']', 'FINISH']
        for e in eee:
            s = s.replace(e, '')
        return s

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
                          {"role": "user", "content": prompt + f'Thought {i}: '}],
                stop=['Thought'],
                temp=0
            )
            try:
                # parse the LLM response
                q, answer = [line.strip() for line in response.split('Answer: ')]
            except:
                # post-processing if the response format is unaligned （See ReAct https://github.com/ysymyth/ReAct/blob/master/hotpotqa.ipynb)
                q = response.strip().split('\n')[0]
                answer = get_from_openai(
                    model=self.model,
                    messages=[{'role': 'system', 'content': GENERATION_SYSTEM},
                              {"role": "user", "content": prompt + f'Thought {i}: {q}\nAnswer: '}],
                    stop=['\n'],
                    temp=0,
                )
                answer = answer.strip().replace('\n', '')

            #  `Finish` is a pre-defined signal in prompt to indicate finish the question
            if 'FINISH' in answer:
                answer = self.noramlize(answer)
                prompt += f"Thought: {q}\nAnswer: {answer}\n"
                return prompt, answer

            q = self.noramlize(q)
            answer = self.noramlize(answer)

            # retrieve document for knowledge augmentation
            raw_doc = Knowledge.get_knowledge(line, mode=self.retrieval, corpus=self.corpus, query=q, k=self.n_docs)

            # sub-question, immediate answer -> calibrated answer
            _answer = self.grounding(q=q, answer=answer, docs=raw_doc, batch=self.batch_doc_size)
            traj = f"Thought {i}: {q}\nAnswer {i}: {_answer}\n"
            print(traj)
            prompt += traj
        return 'NO ANSWER'


