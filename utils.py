import collections
import hashlib

# ハッシュコード生成
print(hashlib.sha256("test".encode()).hexdigest())

# これを使用してブロックになる
block = {"b": 2, "a": 1}
block2 = {"a": 1, "b": 2}


def sorted_dict_by_key(unsorted_dict):
    # keyを並べ替えをする。
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0])
    )


# ブロックごとハッシュ化する
print(hashlib.sha256(str(block).encode()).hexdigest())
