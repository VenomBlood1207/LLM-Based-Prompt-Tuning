from src.data_persistence.database import DatabaseManager
from src.evaluation.metrics1 import (
    MetricsCalculator, calculate_bleu, calculate_rouge, calculate_semantic_similarity
)
import csv

def save_summary_to_csv(summary, filename="evaluation_results.csv"):
    if not summary:
        return
    keys = summary[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(summary)

def save_summary_to_md(summary, filename="evaluation_results.md"):
    if not summary:
        return
    keys = summary[0].keys()
    with open(filename, "w") as f:
        f.write("| " + " | ".join(keys) + " |\n")
        f.write("|" + "|".join(["---"] * len(keys)) + "|\n")
        for row in summary:
            f.write("| " + " | ".join(str(row[k]) for k in keys) + " |\n")

class EvaluationPipeline:
    def __init__(self, db_path="data/optimization.db"):
        self.db = DatabaseManager(db_path)
        self.metrics = MetricsCalculator()

    def evaluate_recent(self, limit=10):
        results = self.db.fetch_recent(limit)
        summary = []
        for row in results:
            orig_prompt, opt_prompt, orig_resp, opt_resp, *_ = row
            metrics = self.metrics.calculate_metrics(orig_prompt, opt_prompt, orig_resp, opt_resp)
            bleu = calculate_bleu(orig_resp, opt_resp)
            rouge = calculate_rouge(orig_resp, opt_resp)
            sim = calculate_semantic_similarity(orig_resp, opt_resp)
            summary.append({
                "prompt": orig_prompt,
                "optimized_prompt": opt_prompt,
                "bleu": bleu,
                "rouge1": rouge['rouge1'].fmeasure,
                "semantic_similarity": sim,
                "custom_improvement": metrics.improvement_ratio
            })
            print(
                f"BLEU: {bleu:.2f}, ROUGE-1: {rouge['rouge1'].fmeasure:.2f}, "
                f"Semantic: {sim:.2f}, Custom: {metrics.improvement_ratio:.2f}"
            )
        return summary

if __name__ == "__main__":
    pipeline = EvaluationPipeline()
    # pipeline.evaluate_recent(limit=5)
    summary = pipeline.evaluate_recent(limit=10)
    # save_summary_to_csv(summary)
    # save_summary_to_md(summary)
    if not summary:
        print("No optimization results found in the database.")
    else:
        save_summary_to_csv(summary)
        save_summary_to_md(summary)
        print(f"Saved {len(summary)} results to evaluation_results.csv and evaluation_results.md")
