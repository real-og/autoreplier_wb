def parse_feedback(feedback_item: dict):
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


from datetime import datetime, timezone

def compose_message(feedback: dict) -> str:
    pd = feedback.get("productDetails") or {}

    fb_id = feedback.get("id", "-")
    user = (feedback.get("userName") or "").strip() or "Без имени"
    rating = feedback.get("productValuation", "-")
    created = feedback.get("createdDate")

    # дата/время: "2026-01-01T09:48:44Z" -> "01.01.2026 09:48"
    created_str = "—"
    if created:
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00")).astimezone(timezone.utc)
            created_str = dt.strftime("%d.%m.%Y %H:%M UTC")
        except Exception:
            created_str = created

    product_name = pd.get("productName", "—")
    brand = pd.get("brandName", "—")
    supplier_article = pd.get("supplierArticle", "—")
    color = feedback.get("color") or "—"
    subject = feedback.get("subjectName") or pd.get("subjectName") or "—"

    text = (feedback.get("text") or "").strip()
    pros = (feedback.get("pros") or "").strip()
    cons = (feedback.get("cons") or "").strip()

    bables = feedback.get("bables") or []
    tags = ", ".join(bables) if isinstance(bables, list) and bables else "—"

    photos = feedback.get("photoLinks") or []
    photos_count = len(photos) if isinstance(photos, list) else 0

    answer = feedback.get("answer")
    answered = "✅ Есть ответ" if answer else "❌ Нет ответа"

    parts = [ 
        f"Время: <b>{created_str}</b>",
        "",
        f"Товар: <b>{product_name}</b>",
        "",
        f"Артикул продавца: <b>{supplier_article}</b>",
        "",
        f"Покупатель: <b>{user}</b>",
        f"Фото: <b>{photos_count}</b>", 
        "",
        f"Оценка: <b>{rating}</b>", 
        f"Теги: <b>{tags}</b>",   
        ""   
    ]

    if text:
        parts += [f"Текст: <b>{text}</b>"]
    if pros:
        parts += [f"Плюсы: <b>{pros}</b>"]
    if cons:
        parts += [f"Минусы: <b>{cons}</b>"]

    if not text and not pros and not cons:
        parts += ["Отзыв без текста"]

    parts += ["", f"ID: <i>{fb_id}</i>"]
    return "\n".join(parts)
