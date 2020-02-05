
# import sys
# from pathlib import Path
# module_path = str(Path(__file__).absolute().parent.parent.parent)
# if module_path not in sys.path:
#     sys.path.append(module_path)  # e.g. '.../repos/<name_of_this_repo>'

from agentbasedmodelspractice.office_training.server import server


if __name__ == '__main__':
    server.launch()
