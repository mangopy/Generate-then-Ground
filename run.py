import argparse
import json
import os
import multiprocessing as mp
import math
from tqdm import tqdm
from src.genground import GenGround
from utilze.metrics import eval_f1, eval_em, eval_acc

def run(process_ids,func, data, args):
    pool = mp.Pool(processes=len(process_ids))
    length = math.ceil(len(data) // len(process_ids))
    collects = []
    for ids, rank in enumerate(process_ids):
        collect = data[ids * length:(ids + 1) * length]
        collects.append(pool.apply_async(func, (rank, args, collect)))
    pool.close()
    pool.join()
    results = []
    for rank, result in zip(process_ids, collects):
        r, res = result.get()
        assert r == rank
        results.extend(res)
    return results


def _run(rank, data, args):
    result = []
    for line in data:
        if 'query' not in line and 'question' in line:
            line['query'] = line.pop('question')
    for i, line in enumerate(tqdm(data[60:100])):
        model = GenGround(model=args.model_name,
                          retrieval=args.retrieval,
                          batch_doc_size=args.batch_doc_size,
                          corpus=args.corpus,
                          n_docs=args.n_docs)
        try:
            traj, res = model.generate(line, corpus='hotpot')
            line['model_response'] = res
            line['traj'] = traj
            print(res, '|||', line['answer'])
            result.append(line)
            json.dump(line, open(f'hotpot-{i}.json'.format(rank), 'w'))
        except:
            print('==================')
    return rank, result

def evaluate(output_folder):
    def _evaluate(preds, answers):
        score = {}
        score['f1'] = eval_f1(preds, [[e] if type(e) == str else e for e in answers])
        score['em'] = eval_em(preds, [[e] if type(e) == str else e for e in answers])
        score['acc'] = eval_acc(preds, [[e] if type(e) == str else e for e in answers])
        print(score)
        return score
    import glob
    files = glob.glob(output_folder + '/*.json')
    answers, predicts = [], []
    for file in files:
        try:
            line = json.load(open(file, 'r'))
            answers.append(line['answer'])
            predicts.append(line['model_response'])
        except:
            pass
    print(len(answers), len(predicts))
    print(_evaluate(predicts, answers))

# evaluate('./hotpot')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default='./dataset/hotpot_distractor_validation.json',
                        help="Path to dataset (.json/.jsonl file)")
    parser.add_argument("--model_name", type=str,default='gpt-3.5-turbo-16k',
                        help="the model name")
    parser.add_argument("--retrieval", type=str,default='oracle',
                        help="how to retrieval docs, i.e, oracle (ground truth), colbert retrieval, etc.")
    parser.add_argument("--batch_doc_size", type=int, default=3,
                        help="the number of docs in batch grounding operation")
    parser.add_argument("--n_docs", type=int, default=9,
                        help="retrieve n_docs most relevant docs for augmentation")
    parser.add_argument("--corpus", type=str, default='wiki',
                        help="retrieve docs from which corpus, i.e., wiki2017/wiki2018")
    parser.add_argument("--num_process", type=int, default=1,
                        help="run multiple parallel processing with DDP strategy to speed the experiment")
    parser.add_argument("--output_file", type=str, default=None,
                        help="file to cache the output results")

    args = parser.parse_args()

    data = json.load(open(args.data_path))

    if args.num_process == 1:
        _, results = _run(rank=list(range(0, 10)),
                          data=data,
                          args=args)
    else:
        results=run(process_ids=list(range(0,args.num_process)),
                    func=_run,
                    data=data,
                    args=args)

    if os.path.exists(args.output_file):
        json.dump(results, open(args.output_file, 'w'), indent=4)