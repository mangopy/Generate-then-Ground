import random
import requests
import json
from tqdm import tqdm
from utilze.data import deprecated

api_search = "http://10.96.202.234:8893"

def document_retrieval(query, k=20):
    url = f'{api_search}/api/search?query={query}&k={k}'
    response = requests.get(url)
    res = response.json()
    knowledge = []
    for doc in res['topk']:
        text = doc['text'][doc['text'].index('|') + 1:].replace('"','').strip()
        title = doc['text'][:doc['text'].index('|')].replace('"','').strip()
        knowledge.append(f"Title: {title}. Content: {text}")
    return knowledge

# This search class has been deprecated
@deprecated
class Knowledge:
    @staticmethod
    def get_knowledge(example, mode='colbert',query='',corpus='hotpot',k=10):
        """

        :param example: dataset sample
        :param mode: oracle: only ground truth, simulation: ground truth + noise, bm25/colbert: search from corpus
        :return: list[document]
        """
        if mode=='bm25':
            pass
        elif mode=='colbert':
            url = 'http://10.102.33.19:8002/search/colbert?query=' + query + f'&k={k}&corpus={corpus}'
            response = requests.get(url)
            res =response.json()
            knowledge = []
            for doc in res['topk']:
                text = doc['text'][doc['text'].index('Text:') + 5:].replace('"','').strip()
                title = doc['text'][:doc['text'].index('Text:')].replace('Title:', '').replace('"','').strip()
                knowledge.append(f"{title}. {text}")
            return knowledge
        elif mode == 'oracle' or mode == 'simulation':
            if example['dataset'] == 'hotpot':
                return Knowledge.get_knowledge_hotpot(example, mode=mode)
            if example['dataset'] == 'multihotpot':
                return Knowledge.get_knowledge_multi_hotpot_qa(example, mode=mode)
            if example['dataset'] == 'hf-wics-strategy':
                return Knowledge.get_knowledge_strategy(example, mode=mode)
            if example['dataset'] == 'musique':
                return Knowledge.get_knowledge_musique(example, mode=mode)
        else:
            raise NotImplementedError

    @staticmethod
    def get_knowledge_strategy(example, mode='oracle'):
        if mode == 'oracle':
            knowledge = example['facts']
        elif mode == 'simulation':
            # ground truth + noise
            knowledge = example['facts'] + example['noise']
            random.shuffle(knowledge)
        else:
            raise NotImplementedError
        return knowledge

    @staticmethod
    def get_knowledge_musique(example, mode='oracle'):
        # ground truth
        # knowledge=[line['paragraph_text'] for line in example['paragraphs'] if line['is_supporting']==True]
        # ground truth + noise
        knowledge = [line['paragraph_text'] for line in example['paragraphs']]
        return knowledge

    @staticmethod
    def get_knowledge_hotpot(example, mode='oracle'):
        if mode=='simulation':
        # ground truth + noise
            knowledge = [t + ' ### ' + ' '.join(s) for t, s in
                     zip(example['context']['title'], example['context']['sentences'])]
        else: # ground truth
            knowledge=[]
            doc_id=[example['context']['title'].index(t) for t in example['supporting_facts']['title']]
            for i in doc_id:
                title=example['context']['title'][i].replace('"','')
                content=' '.join(example['context']['sentences'][i]).replace('"','')
                knowledge.append(f"Title: {title} Text: {content})")

            knowledge=list(set(knowledge))

        return knowledge

    @staticmethod
    def get_knowledge_multi_hotpot_qa(example, mode='oracle'):
        # ground truth
        knowledge= []
        for t in example['supporting_facts']:
            for e in example['context']:
                if e[0]==t[0]:
                    knowledge.append(' '.join(e[1]))
        knowledge=list(set(knowledge))
        return knowledge


