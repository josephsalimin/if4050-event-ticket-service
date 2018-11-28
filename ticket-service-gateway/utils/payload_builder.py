import json


def build_payload(args_dict, var="variables"):
    payload = {var: {}}
    for key in args_dict.keys():
        payload[var][key] = {}
        if isinstance(args_dict[key], dict):
            payload[var][key]["value"] = json.dumps(args_dict[key])
        elif isinstance(args_dict[key], list):
            payload[var][key]["value"] = json.dumps(args_dict[key])
        else:
            payload[var][key]["value"] = args_dict[key]

        if isinstance(args_dict[key], int):        
            payload[var][key]["type"] = "Integer"
        else:
            payload[var][key]["type"] = "String"

    return payload
