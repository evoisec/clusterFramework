# import sampletask2, sampletask22

import importlib

PLUGIN_NAME = "sampletask2"

plugin_module = importlib.import_module(PLUGIN_NAME, ".")

print(plugin_module)

plugin = plugin_module.Plugin("HMM", key=123)

result = plugin.execute(5, 3)

print(result)

PLUGIN_NAME = "sampletask22"

plugin_module = importlib.import_module(PLUGIN_NAME, ".")

print(plugin_module)

plugin = plugin_module.Plugin("SVM", key=333)

result = plugin.execute(5, 3)

print(result)