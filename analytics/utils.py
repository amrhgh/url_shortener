def merge(a, b, path=None):
    "merges b into a"
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key])
            else:
                a[key] += b[key]
        else:
            a[key] = b[key]
    return a


def count_list_items_in_reports(orig_dic, dic_records, dic_unique_records):
    """
    all values of orig_dic are list of ips which visited short urls,
    here counting ips in each category
    :param orig_dic: dictionary that its values are list of ips
    :param dic_records: at first pass an empty dictionary
    :param dic_unique_records: at first pass an empty dictionary
    """
    for key in orig_dic:
        if isinstance(orig_dic[key], dict):
            dic_records[key] = dict()
            dic_unique_records[key] = dict()
            count_list_items_in_reports(orig_dic[key], dic_records[key], dic_unique_records[key])
        else:
            dic_unique_records[key] = len(set(orig_dic[key]))
            dic_records[key] = len(orig_dic[key])
