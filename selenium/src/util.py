from .selenium_driver import SeleniumDriver
import os
import re


class EnvUtil():
    @staticmethod
    def print_all_env(self):
        for k, v in os.environ.items():
            print(f'{k}={v}')

    @staticmethod
    def get_or_raise(self, target_key):
        if not os.environ.get("URL", None) and target_key:
            raise UnconfiguredEnvironment(target_key)


class UnconfiguredEnvironment(Exception):
    def __init__(self, target_key):
        raise Exception(".env error: " + target_key + " does not exist")
