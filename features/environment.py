# -*- coding: utf-8 -*-
from utils.user_session import UserSession
from utils.config import CONFIG
from behave.model_core import Status


def before_all(context):
    context.userSession = UserSession()
    context.userSession.setConfig(CONFIG)
    context.multiBrowser = False
    context.driver = context.userSession.drivers[0]


def after_all(context):
    context.userSession.logOut()
    context.userSession.closeBrowsers()


def before_scenario(context, scenario):
    context.multiBrowser = "multibrowser" in scenario.effective_tags


def before_step(context, step):
    if str(step.filename) == "<string>":
        # skip if this step is a sub-step
        return
    if context.multiBrowser:
        # run the same step in different browsers
        for idx in range(len(context.userSession.drivers) - 1):
            context.driver = context.userSession.drivers[idx]
            try:
                context.execute_steps(str(step)[1:-1].replace('"', ""))
            except Exception as err:
                raise Exception(
                    f"\033[1;35;40m\nTest failed while running in {type(context.driver)}:\n{err}"
                )
        context.driver = context.userSession.drivers[-1]


def after_step(context, step):
    if step.status == Status.failed:
        raise Exception(
            f"\033[1;35;40m\nTest failed while running in {type(context.driver)}:\n{step.error_message}"
        )
