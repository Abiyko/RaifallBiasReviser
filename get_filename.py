import os



def get(orgDirPath):
    try:
        file_names=os.listdir(orgDirPath)
        return file_names
    except:
        print('orgディレクトリのファイルリストを取得できませんでした。')


if __name__=='__main__':
    get()