import collections
import hashlib

# ハッシュコード生成
# print(hashlib.sha256("test".encode()).hexdigest())

# これを使用してブロックになる
block = {"b": 2, "a": 1}
block2 = {"a": 1, "b": 2}


def sorted_dict_by_key(unsorted_dict):
    # keyを並べ替えをする。
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0])
    )



def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"=" * 25} Chain {i} {"=" * 25}')
        '''　↑と表示する
        ========================= Chain 1 =========================
        '''
        for k, v in chain.items():

            if k == "transactions":
                print(k)
                for d in v:
                    print(f'{"-" * 40}')
                    for kk,vv in d.items():
                        print(f"{kk:30}{vv}")
            else:
                print(f'{k:15}{v}')

        print(f'{"*" * 25}')




# ブロックごとハッシュ化する
print(hashlib.sha256(str(block).encode()).hexdigest())
