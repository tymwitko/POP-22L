from GA import recreate
import yaml

def read_files(filename:str) -> list:
    with open(filename+".yaml", 'r') as file:
        files = yaml.safe_load(file)
    return files

def main():
    files = read_files('recreate')
    for file in files:
        print('----------', file, '----------')
        recreate("results/" + str(file))

if __name__ == "__main__":
    main()
