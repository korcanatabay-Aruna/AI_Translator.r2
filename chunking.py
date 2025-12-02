import re
from typing import List

def is_short_sutta(text: str) -> bool:
    return len(text.split()) <= 50

def split_into_chunks(text: str) -> List[str]:
    if is_short_sutta(text):
        return [text]
    # Uzun Sutta’larda bölüm başlıklarına göre ayır
    pattern = r"(BİRİNCİ BÖLÜM:|İKİNCİ BÖLÜM:|ÜÇÜNCÜ BÖLÜM:|DÖRDÜNCÜ BÖLÜM:|BEŞİNCİ BÖLÜM:|ALTINCI BÖLÜM:|İzdeşler!|Kutlu Kişi|Ānanda|Licchaviler|Subhadda)"
    parts = re.split(f"({pattern})", text)
    chunks = []
    current = ""
    for i in range(len(parts)):
        if re.match(pattern, parts[i].strip()):
            if current.strip():
                chunks.append(current.strip())
            current = parts[i]
        else:
            current += parts[i]
    if current.strip():
        chunks.append(current.strip())
    return chunks if len(chunks) > 1 else [text]