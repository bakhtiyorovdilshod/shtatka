def fix_pagination(data, domain_name):
    next = data.get('next')
    previous = data.get('previous')
    domain_name = domain_name.split('?')
    if next:
        split_data = data['next'].split('?')
        split_data[0] = domain_name[0]
        split_data.insert(1, '?')
        data['next'] = ''.join(split_data)
    if previous:
        split_data = data['previous'].split('?')
        split_data[0] = domain_name[0]
        split_data.insert(1, '?')
        data['previous'] = ''.join(split_data)
    return data