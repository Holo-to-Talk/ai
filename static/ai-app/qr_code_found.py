from constants import QRCodeFoundSettings

# 特定単語があるかどうか
def qr_code_found(inputContent):
    # 特定単語取得
    SEARCH_LIST = QRCodeFoundSettings.SEARCH_LIST

    # 特定単語検索
    found = any(char in inputContent for char in SEARCH_LIST)

    # 特定単語があるかどうか
    if found:
        return True

    else:
        return False