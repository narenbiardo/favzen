from models.folder import Folder


class FolderPresenter:
    def __init__(self, view):
        self.view = view

    def load_folders(self):
        folders = Folder.get_all_folders()
        self.view.show_folders(folders)

    def add_folder(self, name, parent_id, icon):
        Folder.add_folder(name, parent_id, icon)
        self.load_folders()

    def update_folder(self, folder_id, name, icon):
        Folder.update_folder(folder_id, name, icon)
        self.load_folders()

    def delete_folder(self, folder_id):
        Folder.delete_folder_recursive(folder_id)
        self.load_folders()
