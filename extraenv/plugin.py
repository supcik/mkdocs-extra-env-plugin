################################################################################
# @file        : plugin.py
# @brief       : Extra Env Plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 15. June 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2022 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT OR Apache-2.0
# ------------------------------------------------------------------------------
# @details
# Extra Env Plugin for MkDocs
################################################################################

import collections.abc
import logging
import os
from datetime import date
from typing import Type

from dotenv import load_dotenv
from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as PluginType
from mkdocs.plugins import BasePlugin

logger = logging.getLogger("mkdocs.plugins." + __name__)
logTag = "[extraenv] -"
load_dotenv(".env")


class ExtraEnvPluginConfig(BaseConfig):
    variables = PluginType(list, default=[])


class ExtraEnvPlugin(BasePlugin[ExtraEnvPluginConfig]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_config(self, config):
        for var in self.config.variables:
            v = var.split(":")
            envVarName = v.pop(0) if len(v) > 0 else ""
            extraVarName = v.pop(0) if len(v) > 0 else ""
            defaultValue = v.pop(0) if len(v) > 0 else ""

            if envVarName == "" and extraVarName == "":
                logger.warn(f"{logTag} variable '{var}' does not have a name")
                continue

            if envVarName == "":
                envVarName = extraVarName.upper()

            if extraVarName == "":
                extraVarName = envVarName.lower()

            value = os.getenv(envVarName, defaultValue)
            config.extra[extraVarName] = value

        return config
