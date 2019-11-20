#!/usr/bin/env python3.7

# DemistoSDK
# Python client that invokes functions in the Demisto SDK.
#
# Author:       Demisto
# Version:      0.1
#

import sys

from .common.tools import print_color, LOG_COLORS
from .yaml_tools.unifier import Unifier
from .yaml_tools.extractor import Extractor
from .common.configuration import Configuration
from .validation.file_validator import FilesValidator


class DemistoSDK:
    SCRIPT = 'script'
    INTEGRATION = 'integration'

    def __init__(self, configuration=Configuration()):
        self.dir_to_prefix = {
            'Integrations': 'integration',
            'Beta_Integrations': 'integration',
            'Scripts': 'script'
        }

        self.configuration = configuration

    def unify_package(self, package_path, dest_path):
        directory_name = ""
        for dir_name in self.dir_to_prefix.keys():
            if dir_name in package_path:
                directory_name = dir_name

        if not directory_name:
            print("You have failed to provide a legal file path, a legal file path "
                  "should contain either Integrations or Scripts directories")
            sys.exit(1)

        unifier = Unifier(package_path, directory_name, dest_path)
        return unifier.merge_script_package_to_yml()

    def migrate_file(self, yml_path: str, dest_path: str, add_demisto_mock=True, add_common_server=True,
                     yml_type=''):
        splitter = Extractor(yml_path, dest_path, add_demisto_mock, add_common_server, yml_type, self.configuration)
        return splitter.migrate()

    def extract_code(self, yml_path: str, dest_path: str, add_demisto_mock=True, add_common_server=True,
                     yml_type=''):
        splitter = Extractor(yml_path, dest_path, add_demisto_mock, add_common_server, yml_type, self.configuration)
        return splitter.extract_code(dest_path)

    def validate(self, **kwargs):
        sys.path.append(self.configuration.content_dir)

        print_color('Starting validating files structure', LOG_COLORS.GREEN)

        validator = FilesValidator(configuration=self.configuration, **kwargs)
        return validator.is_valid_structure()
