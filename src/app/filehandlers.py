import pickle

from ui.utils.filemanager import FileManagerWindow
from context.context_wrapper import ContextWrapper

ctx_wrapper = ContextWrapper()


def save(path):
    with open(f'{path}.fy', 'wb') as f:
        pickle.dump(ctx_wrapper, f)


def load(path):
    with open(f'{path}', 'rb') as f:
        loaded_context = pickle.load(f)
    ctx_wrapper.__dict__.update(loaded_context.__dict__)