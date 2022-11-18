# -*- coding: utf-8 -*-
from utils.user_session import UserSession

"""
Client to interact with file manager's APIs
"""


class FileManagerClient:
    def __init__(self, session: UserSession) -> None:
        self.session = session

    def listFiles(self) -> list[str]:
        pass
