"""

errors.py | YDITS for Discord

Copyright (c) 2022-2023 よね/Yone
Licensed under the Apache License 2.0


"""

class Errors:
    ERRORS = {
        0x0301: "情報の取得がタイムアウトしました。\n",
        0x0302: "JSONの解析に失敗しました。",
        0x0303: "リクエストが多すぎます。",
        0x0304: "HTTP NG が発生しました。",
        0x0305: "JSONのデータアクセスで問題が発生しました。",
    }

    def __init__(self) -> None:
        return
