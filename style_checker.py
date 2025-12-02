def is_ufuk_hoca_style(translation: str) -> bool:
    """
    Verilen çevirinin Ufuk Hoca tarzında olup olmadığını kontrol eder.
    Basit kural tabanlı stil kontrolü.
    """
    conditions = [
        "Duydum ki" in translation,
        "İzdeşler!" in translation,
        "Kutlu Kişi" in translation,
        "!" in translation and ("öfke" in translation.lower() or "efendiniz" in translation.lower()),
        "tıpkı" in translation or "benzet" in translation or "gibi" in translation
    ]
    return any(conditions)