import os

from Utilities import extract_folder


def decompile_all(input_directory: str, output_directory: str):
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    gameplay_folder_data = os.path.join(
        input_directory, "Data", "Simulation", "Gameplay"
    )
    gameplay_folder_game = os.path.join(input_directory, "Game", "Bin", "Python")
    extract_folder(output_directory, gameplay_folder_data)
    extract_folder(output_directory, gameplay_folder_game)


def main():
    input_directory = "E:\\Origin Games\\The Sims 4"
    output_directory = "decompiled"
    decompile_all(input_directory, output_directory)


if __name__ == "__main__":
    main()
