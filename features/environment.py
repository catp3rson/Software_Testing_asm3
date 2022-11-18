# -*- coding: utf-8 -*-
import os
from utils.user_session import UserSession
from utils.config import CONFIG
from utils.file_handler import FileHandler


def before_all(context):
    context.userSession = UserSession()
    context.userSession.setConfig(CONFIG)
    context.config = CONFIG
    context.driver = context.userSession.drivers[0]
    context.fileHandler = FileHandler(CONFIG["DATA_DIR"])


def after_all(context):
    context.userSession.logOut()
    context.userSession.closeBrowsers()


def before_feature(context, feature):
    context.fileHandler.setCwd(os.path.basename(feature.filename).rsplit(".", 1)[0])


def after_feature(context, feature):
    context.fileHandler.cleanUpRandFiles()


def before_scenario(context, scenario):
    if "multibrowser" in scenario.effective_tags:
        steps_text = "\n".join(
            map(lambda x: str(x)[1:-1].replace('"', ""), scenario.all_steps)
        )
        for idx in range(len(context.userSession.drivers) - 1):
            context.driver = context.userSession.drivers[idx]
            try:
                context.execute_steps(steps_text)
            except Exception as err:
                raise Exception(
                    f"\033[1;35;40m\nTest failed while running in {type(context.driver)}:\n{err}"
                )
        context.driver = context.userSession.drivers[-1]
