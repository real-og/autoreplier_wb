def parse_feedback(feedback_item:dict):
    return {
        "userName": feedback_item.get("userName", ""),
        "rating": feedback_item.get("productValuation"),
        "text": feedback_item.get("text", ""),
        "pros": feedback_item.get("pros", ""),
        "cons": feedback_item.get("cons", ""),
        "productName": (feedback_item.get("productDetails") or {}).get("productName", ""),
        "brandName": (feedback_item.get("productDetails") or {}).get("brandName", ""),
        "bables": feedback_item.get("bables", []),
        "color": feedback_item.get("color", ""),
    }