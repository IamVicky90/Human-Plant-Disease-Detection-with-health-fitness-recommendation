import os
def create_directory(dirnames:list,exist_ok=True):
    '''
    args:
        dirnames: expected directory names with path in list
        exist_ok: will not raise except if directory already exists by default True
    '''
    for dir in dirnames:
        try:
            os.makedirs(dir,exist_ok=exist_ok)
            with open(os.path.join(dir,'.gitkeep'),'w+') as f:
                pass
        except Exception as e:
            raise e