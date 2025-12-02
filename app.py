from dotenv import load_dotenv
import os

load_dotenv()

import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"

import gradio as gr
from langgraph_workflow import create_workflow
from rag_utils import setup_vectorstore

api_key = os.getenv("OPENAI_API_KEY")

# Vektör DB'yi hazırla (bir kez çalıştır)
if not os.path.exists("chroma_db"):
    setup_vectorstore()

workflow = create_workflow()

def translate_sutta(input_text: str):
    length_type = "short" if len(input_text.split()) <= 50 else "long"
    state = {
        "source_text": input_text,
        "length_type": length_type,
        "chunks": [],
        "current_chunk_idx": 0,
        "translated_chunks": [],
        "current_translation": "",
        "refinement_round": 0,
        "max_refinement": 2,
        "is_approved": False,
        "final_output": ""
    }
    result = workflow.invoke(state)
    return result["final_output"]

def approve_translation(text):
    return f"✅ Onaylandı! Çeviri kaydedildi.\n\n{text}"

def improve_translation(text):
    # Basit: tekrar çalıştır (gelişmiş versiyonunda refinement_round artırılır)
    return translate_sutta(text)

# Gradio Arayüzü
with gr.Blocks(title="Ufuk Hoca Tarzı Sutta Çevirisi") as demo:
    gr.Markdown("## 🌿 Ufuk Hoca Tarzında Sutta Çevirisi")
    gr.Markdown("İngilizce Sutta metnini girin → Sistem otomatik Türkçeye çevirir → Siz onaylayın!")
    
    with gr.Row():
        input_box = gr.Textbox(label="İngilizce Sutta", lines=10, placeholder="Örn: 'Don’t let anger be your master...'")
        output_box = gr.Textbox(label="Türkçe Çeviri (Ufuk Hoca Tarzı)", lines=10)
    
    with gr.Row():
        translate_btn = gr.Button("🔄 Çevir", variant="primary")
        approve_btn = gr.Button("✅ Onayla", variant="success")
        improve_btn = gr.Button("🔁 Geliştir", variant="secondary")
    
    # İşlevsellik
    translate_btn.click(fn=translate_sutta, inputs=input_box, outputs=output_box)
    approve_btn.click(fn=approve_translation, inputs=output_box, outputs=output_box)
    improve_btn.click(fn=improve_translation, inputs=output_box, outputs=output_box)

    gr.Markdown("### 📥 Yeni Sutta Yükleme")
    gr.Markdown("`.docx` dosyası olarak İngilizce ve Türkçe çevirileri `data/corpus/` klasörüne koyun. Format: `SN11.25.docx` ve `SN11.25.tr.docx`")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)