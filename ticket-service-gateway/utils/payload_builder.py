import json


def build_payload(args_dict):
    payload = {"variables": {}}
    for key in args_dict.keys():
        payload["variables"][key] = {}
        if isinstance(args_dict[key], dict):
            payload["variables"][key]["value"] = json.dumps(args_dict[key])
        elif isinstance(args_dict[key], list):
            payload["variables"][key]["value"] = json.dumps(args_dict[key])
        else:
            payload["variables"][key]["value"] = args_dict[key]

        if isinstance(args_dict[key],str):        
            payload["variables"][key]["type"] = "String"
        else:
            payload["variables"][key]["type"] = "Integer"

    return payload
