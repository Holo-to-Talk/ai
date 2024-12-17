from constants import QRCodeFoundSettings

def qr_code_found(inputContent):
    SEARCH_LIST = QRCodeFoundSettings.SEARCH_LIST

    found = any(char in inputContent for char in SEARCH_LIST)

    if found:
        return True

    else:
        return False