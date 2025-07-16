def handler(event, context):
    """Thêm các thuộc tính mới cho token trước khi tạo token cho
    người dùng. Hàm lambda này không được sử dụng theo dạng HTTPs
    hay REST Trigger.

    Args:
        event (dict): event của lambda
        context (dict): context của lambda

    Returns:
        event: trả về event của lambda
    """
    user_attrs = event["request"]["userAttributes"]

    role = user_attrs.get("custom:role", "")
    full_name = f"{user_attrs.get('given_name', '')} {user_attrs.get('family_name', '')}".strip()

    event["response"] = {
        "claimsAndScopeOverrideDetails": {
            "idTokenGeneration": {
                "claimsToAddOrOverride": {
                    "custom:role": role,
                    "full_name": full_name,
                }
            },
            "accessTokenGeneration": {
                "claimsToAddOrOverride": {
                    "custom:role": role,
                },
                "scopesToAdd": [f"role:{role}"] if role else [],
            },
        }
    }

    return event
