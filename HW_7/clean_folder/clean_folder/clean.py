import shutil
import sys
from pathlib import Path, PurePath


def archive_extr(file_link, extract_dir):  # розпаковує архів в задану папку, потім видаляє архів

    folder_name = file_link.name[:(file_link.name).rfind(".")]
    extract_dir = Path(PurePath(extract_dir, 'archives', folder_name))

    shutil.unpack_archive(file_link, extract_dir)
    file_link.unlink()

    return None


def delete_empty_folders(main_folder):

    tree, folders_list = (get_files_tree_from(main_folder))
    empty_folders_list = []

    for folder in folders_list:
        if not any(Path(folder).iterdir()):
            empty_folders_list.append(folder)
            folder.rmdir()

    if empty_folders_list:
        delete_empty_folders(main_folder)
    else:
        pass

    return None


def get_files_tree_from(direction):  # будує дерево папок\файлів

    tree = {}    # key - розташування, value - список файлів
    files = []
    folders = [direction]    # Список папок
    do_not_touch = ['archives', 'video', 'audio', 'documents', 'images']

    for obj in direction.iterdir():

        if obj.is_dir():

            if obj.name.casefold() in do_not_touch:
                pass

            else:
                tree_1, folders_1 = get_files_tree_from(obj)
                tree.update(tree_1)

                for i in folders_1:
                    folders.append(i)

        elif obj.is_file():
            files.append(obj.name)
            tree[direction] = files

    return tree, folders  # types: dict, list


def move_file_to_folder(file_link, file_type, main_folder):

    dest_folder = Path(PurePath(main_folder, file_type))
    dest_folder.mkdir(exist_ok=True)

    new_file_link = Path(PurePath(dest_folder, file_link.name))
    file_link.replace(new_file_link)

    return None


def tranliteration(file_name):

    ua_cyrillic_symbols = ("а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и",\
                           "і", "ї", "й", "к", "л", "м", "н", "о", "п", "р", "с",\
                           "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я")

    latin_symbols = ("a", "b", "v", "h", "g", "d", "e", "ye", "zh", "z", "y",\
                     "i", "i", "yi", "k", "l", "m", "n", "o", "p", "r", "s",\
                     "t", "u", "f", "kh", "ts", "ch", "sh", "shc", "", "yu", "ya")

    t_dictionary = {}

    for c, l in zip(ua_cyrillic_symbols, latin_symbols):
        t_dictionary[ord(c)] = l
        t_dictionary[ord(c.upper())] = l.upper()

    translated_name = file_name.translate(t_dictionary)

    return translated_name


def normalize(string):

    latin_name = tranliteration(string)     # заміна кирилиці на латинку

    latin_num_and_abc = ''      # залишити тільки '_' і букви\цифри
    for char in latin_name:

        if char.isalnum():
            latin_num_and_abc += char
        else:
            latin_num_and_abc += '_'

    return latin_num_and_abc


def renaming(f_link):

    if f_link.is_file():
        file_name = f_link.name[:(f_link.name).rfind(".")]
        file_ext = f_link.suffix
        norm_file_name = normalize(file_name)

        new_name = f_link.replace(Path(f_link.parent, norm_file_name + file_ext))

    else:
        new_name = f_link

    return new_name


def rename_remaining_folders(main_folder): #  нормалізувати назву папок що залишилися після сортуваня

    tree, folders_list = (get_files_tree_from(main_folder))
    folders_list.sort(reverse=True)

    for folder in folders_list:
        norm_folder_name = normalize(folder.name)
        new_folder = folder.replace(Path(folder.parent, norm_folder_name))

    return None


def sorting_files_to_folders(tree, known_file_extension, main_folder):

    users_files_known_extension = set()
    unknown_file_extension = set()

    files_lists = {
                    'archives': [],
                    'audio': [],
                    'documents': [],
                    'images': [],
                    'video': [],
                    'unknown': []
                    }

    for key, values in tree.items():

        for file in values:

            file_location = renaming(Path(PurePath(key, file)))
            file_suffix = (file_location.suffix).casefold()

            if file_suffix in known_file_extension['archives']:
                files_lists['archives'].append(file_location.name)
                users_files_known_extension.add(file_suffix)
                archive_extr(file_location, main_folder)

            elif file_suffix in known_file_extension['audio']:
                users_files_known_extension.add(file_suffix)
                files_lists['audio'].append(file_location.name)
                ftype = 'audio'
                move_file_to_folder(file_location, ftype, main_folder)

            elif file_suffix in known_file_extension['documents']:
                users_files_known_extension.add(file_suffix)
                files_lists['documents'].append(file_location.name)
                ftype = 'documents'
                move_file_to_folder(file_location, ftype, main_folder)

            elif file_suffix in known_file_extension['images']:
                users_files_known_extension.add(file_suffix)
                files_lists['images'].append(file_location.name)
                ftype = 'images'
                move_file_to_folder(file_location, ftype, main_folder)

            elif file_suffix in known_file_extension['video']:
                users_files_known_extension.add(file_suffix)
                files_lists['video'].append(file_location.name)
                ftype = 'video'
                move_file_to_folder(file_location, ftype, main_folder)

            else:
                files_lists['unknown'].append(file_location.name)
                unknown_file_extension.add(file_suffix)

    delete_empty_folders(main_folder)       # видалити всі пусті папки
    rename_remaining_folders(main_folder)   # перейменувати папки що залишилися

    return files_lists, list(users_files_known_extension), list(unknown_file_extension)




def cleaning():
    
    known_file_extension = {
                            'archives': ['.zip', '.gz', '.tar'],
                            'audio': ['.mp3', '.ogg', '.wav', '.amr'],
                            'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
                            'images': ['.jpeg', '.png', '.jpg', '.svg'],
                            'video': ['.avi', '.mp4', '.mov', '.mkv']
                            }

    # Приймаємо аргумент і перевіряєм чи це дійсно шлях на папку
    try:
        main_folder_path = Path(sys.argv[1])

        if main_folder_path.is_dir():
            print(f'\nYour parent folder is: {main_folder_path}\n')

        else:
            raise Exception("This path doesn't exist.")

    except IndexError:
        print('No argument.')


    tree, folders_list = (get_files_tree_from(main_folder_path))

    sorted_files_lists, known_file_ext, unknown_file_ext = sorting_files_to_folders(tree, known_file_extension, main_folder_path)

    
    
    print('\n--------- Список файлів у кожній категорії ---------\n')
    for categoty, files in sorted_files_lists.items():
        files.sort()
        print(f'{categoty}\n{files}\n\n')

    print(f'\n----------- Список відомих розширень ------------\n{known_file_ext}')
    print(f'\n----------- Список невідомих розширень ----------\n{unknown_file_ext}')


if __name__ == '__main__':
    cleaning()
