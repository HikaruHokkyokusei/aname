import os
import traceback
from warnings import filterwarnings

# noinspection PyPackageRequirements
from mal import AnimeSearch

filterwarnings("ignore")
replace_set = {
    "\\": "∖",
    "\"": "ʺ",
    ":": "꞉",
    "<": "＜",
    ">": "＞",
    "/": "Ⳇ",
    "*": "＊",
    "?": "ॽ",
    "!": "ⵑ"
}


def get_original_anime_name(anime_name: str, max_results: int = 5) -> str | None:
    print('\n' + anime_name.title())

    counter, choice = 1, 0
    results = AnimeSearch(anime_name).results
    for result in results:
        print(str(counter) + ' - ' + result.title)
        if counter == max_results:
            break
        counter += 1
    print("X - Skip this folder")

    choice = input('> ')
    if choice == '':
        choice = 1
    elif choice.upper() == "X":
        return None
    choice = int(choice) - 1

    return results[choice].title


if __name__ == "__main__":
    max_res = input("Max Results (default 5): ")
    try:
        max_res = int(max_res)
    except ValueError:
        max_res = 5

    folder_list = next(os.walk('.'))[1]
    if folder_list is None or len(folder_list) == 0:
        print("No folders in the current directory")
        exit()

    for folder in folder_list:
        # Extracting the name of the folder without the path and then performing search for the same.
        # This will be the name of the anime episode, thus instead of performing a search for the directory path,
        # now performing a search for the directory name.
        name = folder.strip().rpartition('\\')[2].strip()
        prefix = name[:name.index(" (")]
        suffix = name[name.index(" ("):]

        original_anime_name = get_original_anime_name(prefix, max_results=max_res).strip()
        if not original_anime_name:
            print("Skipping this folder...")
            continue
        else:
            print("Currently selected name: " + original_anime_name)
            is_satisfied = input("Continue with current name (Y/N)? ")
            if is_satisfied != "y" and is_satisfied != "Y" and is_satisfied != "":
                original_anime_name = input("Enter your preferred name: ")

        final_name = ""
        for char in original_anime_name:
            replacement = replace_set.get(char, None)
            if replacement is None:
                replacement = char
            final_name += replacement

        try:
            os.rename(folder, final_name.strip() + suffix)
        except Exception as e:
            print('Error while renaming the folder')
            for line in traceback.format_exception(None, e, e.__traceback__):
                print(line, end="")
            continue
