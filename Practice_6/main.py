import webbrowser
import zlib


def get_file_content(sha, path):
    try:
        # Получаем путь к объекту Git по его хэшу
        object_path = path + f'.git\\objects\\{sha[:2]}\\{sha[2:]}'
        # Читаем сжатые данные из файла
        with open(object_path, 'rb') as file:
            compressed_data = file.read()
        # Декомпрессия данных
        decompressed_data = zlib.decompress(compressed_data)
        # Получаем тип и размер объекта
        header_end = decompressed_data.index(b'\x00') + 1
        header = decompressed_data[:header_end].decode('utf-8')
        obj_type, obj_size = header.split()
        # Получаем содержимое файла
        content = decompressed_data[header_end:]
        return content.decode('utf-8')
    except FileNotFoundError:
        print(object_path)
        return f'Error: Object not found'
    except IOError as e:
        return f'Error: {e}'


def get_commits(commit, path, buffer=""):
    nextLine = "%3B%0A%20%20"
    data = str(get_file_content(commit, path))
    lines = str(data).splitlines()
    for line in lines:
        if (line.startswith("parent")):
            buffer += "\"" + str(commit) + "\" -> \"" + str(line.split(" ")[1] + "\"" + nextLine)
            buffer = get_commits(line.split(" ")[1], path, buffer)
    print(line)
    return buffer


def format(buff):
    nextLine = "%3B%0A%20%20"
    buff = buff.split(nextLine)
    old_lines = []
    new_str = ""
    for i in range(0, len(buff)):
        line = buff[i]
        if (not (line in old_lines)):
            old_lines.append(line)
            new_str += line
    return new_str


if __name__ == "__main__":
    graphizSite = "https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0A%20%20"
    graphizSite2 = "%0A%7D"
    print("Path to local git rep")
    path = str(input())
    git_dir = path + '.git\\refs\\heads\\main'
    with open(git_dir, 'r') as f:
        commit = f.read().strip()
        buff = get_commits(commit, path)
    buff = format(buff)
    webbrowser.open(graphizSite + buff + graphizSite2)