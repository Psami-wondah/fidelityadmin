def user_serialize_dict(a) -> dict:
    return {
        **{"id": str(a[i]) for i in a if i == "_id"},
        **{"wallet": str(a[i]) for i in a if i == "wallet"},
        **{i: a[i] for i in a if i != "_id" and i != "wallet" and i != "plans"},
        **{"plans": serialize_plans(a[i]) for i in a if i == "plans"},
    }


def user_serialize_list(a) -> list:
    return [user_serialize_dict(i) for i in a]


def serialize_plans(a) -> list:
    return [str(i) for i in a]
