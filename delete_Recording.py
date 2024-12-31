import os

# 作成したファイル削除
def delete_Recording(savedDirectory):
    # ファイルが存在するか
    if os.path.exists(savedDirectory):
        # ファイル削除
        os.remove(savedDirectory)