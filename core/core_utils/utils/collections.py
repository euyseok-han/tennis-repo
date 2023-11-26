def deep_update(base_dict, update_with):
    for key, value in update_with.items():
        if isinstance(value, dict):
            if isinstance(base_dict_value := base_dict.get(key), dict):
                deep_update(base_dict_value, value)
            else:
                base_dict[key] = value
        else:
            base_dict[key] = value
    return base_dict