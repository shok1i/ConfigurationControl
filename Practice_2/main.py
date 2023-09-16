import zipfile

# Иерархическое древо
class PyElement:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def digraph(self):

        for child in self.children:
            print(" " * 6 + self.name + " -> ", end='')
            print(child.name)

        for child in self.children:
            child.digraph()


    def graph(self):
        if self.children:
            print(" " * 7 + self.name + " -- { ", end='')
            temp = self
            i = 0
            for child in self.children:
                # child.display(indent + 4)
                if (i != 0): print(', ', end='')
                print(child.name, end='')
                i += 1
            print(" }")
            for child in temp.children:
                child.graph()


    def find_element(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.find_element(name)
            if result:
                return result
        return None

# Получаем пути у каждого найденого файла
def get_full_path(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_names = zip_ref.namelist()
        for file_name in file_names:
            path_cut(file_name)

# Обрезаем и добавляем в нужное место в древе иерархии
def path_cut(filename):
    while "/" in filename:
        cut = filename.split("/", 1)[0]
        filename = filename.split("/", 1)[1]

        target_element = root.find_element(cut)
        if target_element and not (root.find_element(filename.split("/", 1)[0])):
            new_element = PyElement(filename.split("/", 1)[0])
            target_element.add_child(new_element)


if __name__ == "__main__":
    root = PyElement("Windows11")
    zip_file_path = "Windows11.zip"
    get_full_path(zip_file_path)

    print("digraph " + zip_file_path + "{")
    root.digraph()
    print("}")
