from configparser import ConfigParser

def read_db_config(filename='./week03/config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise Exception('{} is not found in file {}'.format(section, filename))

    return dict(items)

if __name__ == '__main__':
    print(read_db_config())