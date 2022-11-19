# -*- coding: utf-8 -*-
import os
import shutil
from behave.runner import Context
from typing import Union


class FileHandler:
    def __init__(self, dataDir: str) -> None:
        self.randFiles = dict()
        self.dataDir = dataDir
        self.cwd = dataDir

    def setCwd(self, dir: str) -> None:
        """
        Set the current working directory.
        The directory must lie within self.dataDir
        Generated files will be stored in this directory.
        """
        self.cwd = os.path.join(self.dataDir, dir)
        if not os.path.isdir(self.cwd):
            os.mkdir(self.cwd)

    def prepareFile(
        self,
        context: Context,
        filename: str,
        rand_suffix: bool = True,
        basename: bool = False,
    ) -> Union[tuple[str, str], str]:
        """
        Prepare file to test uploading.
        Return absolute path to the pepared file.
        """
        file = os.path.join(self.cwd, filename)
        if not os.path.exists(file):
            return None
        if rand_suffix:
            key = f"{context.scenario}-{context.feature}-{type(context.driver)}"
            name, ext = filename.split(".", 1)
            randFilename = f"{name}-{os.urandom(8).hex()}.{ext}"
            randFile = os.path.join(self.cwd, randFilename)
            if key in self.randFiles:
                self.randFiles[key][file] = randFile
            else:
                self.randFiles[key] = {file: randFile}
            shutil.copyfile(file, randFile)
            if basename:
                return (randFile, os.path.basename(randFile))
            else:
                return randFile
        else:
            if basename:
                return (file, os.path.basename(file))
            else:
                return file

    def getRandFile(
        self, context: Context, file: str, basename: bool = False
    ) -> Union[tuple[str, str], str]:
        """
        Get absolute path to a generated file that was prepared previously.
        """
        key = f"{context.scenario}-{context.feature}-{type(context.driver)}"
        if not os.path.isabs(file):
            file = os.path.join(self.cwd, file)
        if key in self.randFiles and file in self.randFiles[key]:
            randFile = self.randFiles[key][file]
            if basename:
                return (randFile, os.path.basename(randFile))
            else:
                return randFile
        return None

    def cleanUpRandFiles(self) -> None:
        """
        Delete all generated random files
        """
        for item in self.randFiles.values():
            for randFile in item.values():
                os.remove(randFile)
