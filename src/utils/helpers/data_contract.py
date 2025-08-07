def transform_dc_res_from_list_api(dc_res: dict):
    """Transform output from List Object API Response to standard response

    Args:
        dc_res (dict): a brief data contract

    Returns:
        dict: transformed brief data contract
    """
    partial_object_key = dc_res.get("Key", "").split("/")
    pok_len = len(partial_object_key)
    partial_name = partial_object_key[pok_len - 1].split(".")

    return {
        "name": partial_name[0],
        "state": partial_object_key[pok_len - 2],
        "updatedAt": dc_res.get("LastModified", ""),
    }


def transform_dc_res_from_head_api(dc_res: dict):
    """Transform output from Head/Get Object API Response to standard response

    Args:
        dc_res (dict): full information of data contract

    Returns:
        dict: transformed data contract
    """
    meta = dc_res.get("Metadata", {})

    version = dc_res.get("VersionId")

    if version == "null" or version is None:
        version = "latest"

    return {
        "version": version,
        "owner": meta.get("uploader"),
        "team": meta.get("team"),
        "updatedAt": dc_res.get("LastModified", ""),
    }
