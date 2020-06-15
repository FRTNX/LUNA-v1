

def queue_for_extraction(target):
    f = open('extraction_list.txt', 'a')
    f.write(f'{target}\n')
    f.close()


def fetch_passive_extraction_list():
    file = open('extraction_list.txt', 'r').read()
    extraction_list = file.split('\n')
    targets = ""
    for i in extraction_list:
        if i != '':
            if ' ' in i:
                targets += f" '{i}'"
            else:
                targets += f' {i}'
    return targets.strip()