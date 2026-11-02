from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Model Comparison API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_PATH = Path(__file__).parent.parent / "rag_feedback.csv"


def load_data():
    if not CSV_PATH.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(CSV_PATH).fillna("")
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


@app.get("/")
def home():
    return {"message": "RAG Dashboard API is running"}


@app.get("/records")
def get_records():
    df = load_data()
    if df.empty:
        return []
    return df.to_dict(orient="records")


@app.get("/summary")
def get_summary():
    df = load_data()

    if df.empty:
        return {
            "total_questions": 0,
            "total_models": 0,
            "average_response_time": 0,
            "accuracy": 0,
            "models": [],
        }

    required = {
        "model", "feedback", "total_seconds"
    }
    missing = required - set(df.columns)
    if missing:
        return {
            "total_questions": len(df),
            "total_models": 0,
            "average_response_time": 0,
            "accuracy": 0,
            "models": [],
            "error": f"CSV is missing columns: {', '.join(sorted(missing))}",
        }

    df["total_seconds"] = pd.to_numeric(
        df["total_seconds"], errors="coerce"
    )
    df["feedback"] = df["feedback"].astype(str).str.strip()

    models = []
    for model, group in df.groupby("model"):
        rated = group[group["feedback"].isin(["Correct", "Incorrect"])]
        correct = int((rated["feedback"] == "Correct").sum())
        incorrect = int((rated["feedback"] == "Incorrect").sum())
        rated_count = len(rated)

        avg_time = group["total_seconds"].mean()

        models.append({
            "model": str(model),
            "total_questions": int(len(group)),
            "correct": correct,
            "incorrect": incorrect,
            "not_rated": int(len(group) - rated_count),
            "accuracy": round(correct / rated_count * 100, 2) if rated_count else 0,
            "average_response_time": round(float(avg_time), 2) if pd.notna(avg_time) else 0,
        })

    total_correct = sum(m["correct"] for m in models)
    total_rated = sum(m["correct"] + m["incorrect"] for m in models)
    valid_times = df["total_seconds"].dropna()

    return {
        "total_questions": int(len(df)),
        "total_models": len(models),
        "average_response_time": round(float(valid_times.mean()), 2) if not valid_times.empty else 0,
        "accuracy": round(total_correct / total_rated * 100, 2) if total_rated else 0,
        "models": models,
    }
