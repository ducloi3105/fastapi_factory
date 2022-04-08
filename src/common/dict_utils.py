from .constants import DICT_KEY_SEPARATOR


def get_diff_keys(from_keys, to_keys, absolute=True):
    result = []

    for fk in from_keys:
        is_ok = True
        for tk in to_keys:
            if absolute:
                str_fk = DICT_KEY_SEPARATOR.join(fk)
                str_tk = DICT_KEY_SEPARATOR.join(tk)
                if str_tk == str_fk:
                    is_ok = False
                    break
            else:
                if tk[0] == fk[0]:
                    is_ok = False
                    break

        if not is_ok:
            continue

        result.append(fk)

    return result


def dive_to_get_value(data, path, default=None):
    key = path[0]
    value = data.get(key)

    if not value:
        return default

    if len(path) == 1:
        return value

    if not isinstance(value, dict):
        raise TypeError('Can only dive to dict')

    return dive_to_get_value(value, path[1:], default)


def dive_to_set_value(data: dict, path: list, value: any = None):
    key = path[0]

    if len(path) == 1:
        data[key] = value
        return

    if key not in data:
        data[key] = {}

    return dive_to_set_value(data[key], path[1:], value)


def copy_value_by_path(origin,
                       path,
                       result,
                       current_level=None):
    if not path:
        return result

    if not current_level:
        current_level = []

    key = path[0]
    if key not in origin:
        return result

    value = origin.get(key)
    current_level.append(key)

    if not value or len(path) == 1:
        dive_to_set_value(result, current_level, value)
        return result

    if isinstance(value, list):
        current_data = dive_to_get_value(result, current_level, [])
        path = path[1:]

        for index, i in enumerate(value):
            if isinstance(i, list):
                raise ValueError(
                    'Unsupported list nested inside list at key: %s' % key)

            try:
                v = current_data[index]
            except IndexError:
                v = None

            if not isinstance(i, dict):
                try:
                    current_data[index] = i
                except IndexError:
                    current_data.append(i)
                continue

            if not v:
                v = {}
                current_data.append(copy_value_by_path(i, path, v))
            else:
                current_data[index] = copy_value_by_path(i, path, v)

        dive_to_set_value(result, current_level, current_data)

    return copy_value_by_path(value, path[1:], result, current_level)


def flatten_keys(data, pre=None):
    pre = pre[:] if pre else []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                for d in flatten_keys(value, pre + [key]):
                    yield d
            elif isinstance(value, (list, tuple, set)):
                if not len(value):
                    continue
                v = value[0]
                for d in flatten_keys(v, pre + [key]):
                    yield d
            else:
                yield pre + [key]
    else:
        yield pre


def filter_keys(data: dict,
                include_keys: list = None,
                exclude_keys: list = None,
                absolute: bool = True):
    if not include_keys and not exclude_keys:
        return data

    if include_keys is None:
        include_keys = []
    if exclude_keys is None:
        exclude_keys = []

    result = dict()

    ild_keys = list(map(
        lambda f: f.split(','),
        include_keys
    ))

    eld_keys = list(map(
        lambda f: f.split(','),
        exclude_keys
    ))

    if ild_keys:
        result_keys = ild_keys
    else:
        result_keys = list(flatten_keys(data))
        result_keys = get_diff_keys(
            result_keys,
            eld_keys,
            absolute=absolute
        )

    for k in result_keys:
        result = copy_value_by_path(data, k, result)
    return result


def flatten_dict(data):
    return dict(
        (DICT_KEY_SEPARATOR.join(k), dive_to_get_value(data=data, path=k))
        for k in flatten_keys(data=data)
    )


def merge_dicts(from_dict: dict,
                to_dict: dict) -> dict:
    flattened_values = flatten_dict(from_dict)

    for key, value in flattened_values.items():
        dive_to_set_value(
            data=to_dict,
            path=key.split(DICT_KEY_SEPARATOR),
            value=value
        )
    return to_dict
