import pytest
from maidchan_http import 占って

@pytest.mark.parametrize("birthday, expect", [
    ("おひつじ座", 0), ("牡羊座", 0), ("0321", 0), ("0419", 0),
    ("おうし座", 1), ("牡牛座", 1), ("0420", 1), ("0520", 1),
    ("ふたご座", 2), ("双子座", 2), ("0521", 2), ("0621", 2),
    ("かに座", 3), ("蟹座", 3), ("0622", 3), ("0722", 3),
    ("しし座", 4), ("獅子座", 4), ("0723", 4), ("0822", 4),
    ("おとめ座", 5), ("乙女座", 5), ("0823", 5), ("0922", 5),
    ("てんびん座", 6), ("天秤座", 6), ("0923", 6), ("1023", 6),
    ("さそり座", 7), ("蠍座", 7), ("1024", 7), ("1121", 7),
    ("いて座", 8), ("射手座", 8), ("1122", 8), ("1222", 8),
    ("やぎ座", 9), ("山羊座", 9), ("1223", 9), ("0119", 9),
    ("みずがめ座", 10), ("水瓶座", 10), ("0120", 10), ("0218", 10),
    ("うお座", 11), ("魚座", 11), ("0219", 11), ("0320", 11),
])
def test_calc_index(birthday, expect):
    assert 占って._calc_index(birthday[-4:]) == expect