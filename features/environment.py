# -*- coding: utf-8 -*-
import os
from utils.config import CONFIG
from utils.file_handler import FileHandler
from utils.driver_handler import DriverHandler


def before_all(context):
    context.driverHandler = DriverHandler(CONFIG["DRIVERS"])
    context.fileHandler = FileHandler(CONFIG["DATA"])


def after_all(context):
    del context.driverHandler
    del context.fileHandler


def before_feature(context, feature):
    context.fileHandler.setCwd(os.path.basename(feature.filename).rsplit(".", 1)[0])
    context.multiBrowser = "multibrowser" in feature.tags


def before_scenario(context, scenario):
    if context.multiBrowser or "multibrowser" in scenario.tags:
        steps_text = "\n".join(
            map(lambda x: str(x)[1:-1].replace('"', ""), scenario.all_steps)
        )
        drivers = context.driverHandler.listDrivers()
        for idx in range(len(drivers) - 1):
            context.driver = drivers[idx]
            try:
                context.execute_steps(steps_text)
            except Exception as err:
                raise Exception(
                    f"\033[1;35;40m\nTest failed while running in {type(context.driver)}:\n{err}"
                )
        context.driver = drivers[-1]
    else:
        context.driver = context.driverHandler.getDefaultDriver()
