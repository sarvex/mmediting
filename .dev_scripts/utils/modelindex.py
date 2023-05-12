import os.path as osp

import mmengine
from modelindex.models.Collection import Collection
from modelindex.models.Model import Model


def dump_yaml_and_check_difference(obj, file):
    """Dump object to a yaml file, and check if the file content is different
    from the original.

    Args:
        obj (any): The python object to be dumped.
        file (str): YAML filename to dump the object to.
    Returns:
        Bool: If the target YAML file is different from the original.
    """

    str_dump = mmengine.dump(
        obj, None, file_format='yaml', sort_keys=True,
        line_break='\n')  # force use LF

    if osp.isfile(file):
        file_exists = True
        # print(f'    exist {file}')
        with open(file, 'r', encoding='utf-8') as f:
            str_orig = f.read()
    else:
        file_exists = False
        str_orig = None

    if file_exists and str_orig == str_dump:
        is_different = False
    else:
        is_different = True
        print(f'    update {file}')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str_dump)

    return is_different


def collate_metrics(keys):
    """Collect metrics from the first row of the table.

    Args:
        keys (List): Elements in the first row of the table.

    Returns:
        dict: A dict of metrics.
    """
    return {
        key: idx
        for idx, key in enumerate(keys)
        if key not in ['Model', 'Dataset', 'Training Resources', 'Download']
    }


def found_table(lines, i):
    if i + 1 >= len(lines):
        return False
    if i < 2 or 'SKIP THIS TABLE' in lines[i - 2]:
        return False
    if lines[i][0] != '|':
        return False

    return any(c in lines[i + 1] for c in ['| :', '|:', '|-'])


def modelindex_to_dict(model):
    if isinstance(model, Collection):
        result = model.data
        if model.metadata is not None:
            result['Metadata'] = model.metadata.data
    elif isinstance(model, Model):
        result = model.data
        if model.metadata is not None:
            result['Metadata'] = model.metadata.data
        if model.results is not None:
            results_list = [r.data for r in model.results]
            result['Results'] = results_list
    return result
