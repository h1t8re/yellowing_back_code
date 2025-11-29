import subprocess

def runcommand(command=[], input_data=b'', timeout="5"):
    try:
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        std_out, std_err = proc.communicate(input=b''+input_data)
        std_out = std_out.strip()
    except FileNotFoundError:
        print("Error running command")
        exit()
    proc.kill()
    return std_out, std_err

def list_directories(root_directory=""):
    ls_stdout, ls_stderr = runcommand(["ls", "-l", root_directory])
    ls_stdout  = ls_stdout.decode("utf-8")
    lines_ls_stdout = ls_stdout.split("\n")
    for line_ls_stdout in lines_ls_stdout:
        words_line_ls_stdout = line_ls_stdout.split(" ")
        if 'd' in words_line_ls_stdout[0]:
            directory_stream = root_directory+"/"+words_line_ls_stdout[-1]
            for directory in list_directories(directory_stream):
                yield directory
            yield directory_stream

def list_files(root_directory=""):
    ls_stdout, ls_stderr = runcommand(["ls", "-l", root_directory])
    ls_stdout  = ls_stdout.decode("utf-8")
    lines_ls_stdout = ls_stdout.split("\n")
    lines_ls_stdout = [line for line in lines_ls_stdout if "total" not in line]
    for line_ls_stdout in lines_ls_stdout:
        words_line_ls_stdout = line_ls_stdout.split(" ")
        if words_line_ls_stdout[1] == '1':
            yield words_line_ls_stdout[-1]

def yellowing_directories(root_directory=""):
    yield root_directory
    for directory_stream in list_directories(root_directory):
        yield directory_stream

def clean_code():
    for stream_to_directory in yellowing_directories("."):
        for file in list_files(stream_to_directory):
            path_file = stream_to_directory+"/"+file
            path_file_backup = path_file+".backup"
            try:
                extension = path_file.split(".")
            except:
                pass
            if extension[-1] in ["py", "c", "h"]:
                print("Cleaning file : "+path_file, end="\n")
                with open(path_file, 'r') as file:
                    with open(path_file_backup, 'w') as file_backup:
                        for information_to_restore in file.read():
                            file_backup.write(information_to_restore)
                with open(path_file_backup, 'r') as file_backup:
                    with open(path_file,'w') as file:
                        for information in file_backup.read():
                            file.write(information)
                runcommand(["rm", "-v", path_file_backup])

def main():
    clean_code()

if __name__ == "__main__":
    main()
