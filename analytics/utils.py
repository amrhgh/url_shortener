def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            else:
                a[key] += b[key]
        else:
            a[key] = b[key]
    return a


def count_list_items_in_reports(orig_dic, dic_records):
    for key in orig_dic:
        if isinstance(orig_dic[key], dict):
            dic_records[key] = dict()
            count_list_items_in_reports(orig_dic[key], dic_records[key])
        else:
            dic_records[key] = len(orig_dic[key])
