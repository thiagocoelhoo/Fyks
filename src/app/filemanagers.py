import pickle

from ui.utils.filemanager import FileManagerWindow
from context.context import Context


class SaveWindow(FileManagerWindow):
    def submit(self):
        ctx = Context(0, 0, 0, 0)
        filename = self.entry.text
        
        with open(f'{self.path}\\{filename}.fyks', 'wb') as f:
            pickle.dump(ctx, f)
        self.close()


class LoadWindow(FileManagerWindow):
    def submit(self):
        ctx = Context(0, 0, 0, 0)
        filename = self.entry.text
        
        with open(f'{self.path}\\{filename}.fyks', 'rb') as f:
            ctx_ = pickle.load(f)
            
        ctx.objects = ctx_.objects
        self.close()
