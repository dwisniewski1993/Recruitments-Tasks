import os


class Image:
    def __init__(self, index: int, file_name: str, path: str) -> None:
        self.id = index
        self.name = file_name
        self.path = path


class Images:
    def __init__(self, main_dir: str) -> None:
        self.working_directory = f"{main_dir}\\Images"
        files = self.get_files(self.working_directory)
        self.images_list = [Image(index=int(file.split('\\')[-1].split('_')[0]),
                                  file_name=file.split('\\')[-1].split('_')[1:][0],
                                  path=file) for file in files if file.split('.')[-1] != 'py']
        ids_list = [int(file.split('\\')[-1].split('_')[0]) for file in files if file.split('.')[-1] != 'py']
        if len(ids_list) == 0:
            self.cur_id = 0
        else:
            self.cur_id = max(ids_list)

    @staticmethod
    def get_files(path: str) -> list:
        return ['\\'.join([path, file]) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

    def get_images_list(self) -> list:
        return [image.__dict__ for image in self.images_list]

    def increase_id(self) -> None:
        self.cur_id += 1

    def add_image(self, image: Image) -> None:
        self.images_list.append(image)
