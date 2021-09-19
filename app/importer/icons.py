import base64


def load_icon_to_base64(icon_path: str):
    icon_base64 = base64.b64encode(open(icon_path, "rb").read()).decode(
        "utf-8"
    )
    return f"data:image/png;base64,{icon_base64}"
