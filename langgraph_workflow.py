from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from chunking import split_into_chunks
from rag_utils import retrieve_context
from style_checker import is_ufuk_hoca_style
import operator

class TranslationState(TypedDict):
    source_text: str
    length_type: str
    chunks: List[str]
    current_chunk_idx: int
    translated_chunks: List[str]
    current_translation: str
    refinement_round: int
    max_refinement: int
    is_approved: bool
    final_output: str

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

# Node: Chunking
def node_split(state: TranslationState):
    chunks = split_into_chunks(state["source_text"])
    return {"chunks": chunks, "current_chunk_idx": 0}

# Node: Retrieve
def node_retrieve(state: TranslationState):
    idx = state["current_chunk_idx"]
    query = state["chunks"][idx] if "chunks" in state else state["source_text"]
    context = retrieve_context(query, state["length_type"])
    return {"current_translation": "", "retrieved_context": context}

# Node: Translate
def node_translate(state: TranslationState):
    idx = state["current_chunk_idx"]
    src = state["chunks"][idx] if "chunks" in state else state["source_text"]
    context = state.get("retrieved_context", [""])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Ufuk Hoca tarzında, samimi, öğretici, günlük dile yakın, metinde 'Duydum ki', 'İzdeşler!', 'Kutlu Kişi' gibi kalıplar olacak şekilde çevir."),
        ("user", f"Bağlam çeviriler:\n{context[0][:500]}\n\nYeni metin:\n{src}")
    ])
    chain = prompt | llm
    trans = chain.invoke({}).content
    return {"current_translation": trans, "refinement_round": 0}

# Node: Style Check
def node_style_check(state: TranslationState):
    approved = is_ufuk_hoca_style(state["current_translation"])
    return {"is_approved": approved}

# Node: Refine
def node_refine(state: TranslationState):
    idx = state["current_chunk_idx"]
    src = state["chunks"][idx] if "chunks" in state else state["source_text"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Bu çeviriyi daha Ufuk Hoca tarzına sok: 'Duydum ki', 'İzdeşler!', emir kipi, görsel benzetmeler, günlük ve öğretici dil."),
        ("user", f"Orijinal: {src}\nMevcut: {state['current_translation']}")
    ])
    chain = prompt | llm
    refined = chain.invoke({}).content
    return {"current_translation": refined, "refinement_round": state["refinement_round"] + 1}

# Conditional Edges
def should_refine(state: TranslationState):
    if state["is_approved"] or state["refinement_round"] >= state["max_refinement"]:
        if "chunks" in state and state["current_chunk_idx"] + 1 < len(state["chunks"]):
            return "next_chunk"
        else:
            return "merge"
    return "refine"

def next_chunk(state: TranslationState):
    return {"current_chunk_idx": state["current_chunk_idx"] + 1}

def merge_output(state: TranslationState):
    if "chunks" in state:
        final = "\n\n".join(state["translated_chunks"] + [state["current_translation"]])
    else:
        final = state["current_translation"]
    return {"final_output": final}

# Graph
def create_workflow():
    workflow = StateGraph(TranslationState)
    workflow.add_node("split", node_split)
    workflow.add_node("retrieve", node_retrieve)
    workflow.add_node("translate", node_translate)
    workflow.add_node("style_check", node_style_check)
    workflow.add_node("refine", node_refine)
    workflow.add_node("next_chunk", next_chunk)
    workflow.add_node("merge", merge_output)

    workflow.set_entry_point("split")
    workflow.add_edge("split", "retrieve")
    workflow.add_edge("retrieve", "translate")
    workflow.add_edge("translate", "style_check")
    workflow.add_conditional_edges("style_check", should_refine, {
        "refine": "refine",
        "next_chunk": "next_chunk",
        "merge": "merge"
    })
    workflow.add_edge("refine", "style_check")
    workflow.add_edge("next_chunk", "retrieve")
    workflow.add_edge("merge", END)
    return workflow.compile()