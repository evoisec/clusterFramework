import sys
import sampletask as mod

mod.trainMLModel("HMM_1")

sys.exit(0)




module = __import__(module_name)
my_class = getattr(module, class_name)
instance = my_class()


class DynamicImporter:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, module_name, class_name):
        """Constructor"""
        module = __import__(module_name)
        my_class = getattr(module, class_name)
        instance = my_class()
        print
        instance


if __name__ == "__main__":
    DynamicImporter("decimal", "Context")