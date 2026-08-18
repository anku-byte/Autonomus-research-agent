import os
from typing import Dict, Any
from graph.state import AgentState
from db.database import save_research_run
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def exporter_node(state: AgentState) -> Dict[str, Any]:
    """
    Converts state["final_report"] (Markdown) into a styled PDF file 
    and persists the completed research run into SQLite memory.
    """
    report_md = state.get("final_report", "")

    print("\n--- Executing Exporter Node (PDF Generation) ---")

    if not report_md:
        print("[EXPORTER ERROR] No report content found to export.")
        return {"pdf_path": ""}

    os.makedirs("outputs", exist_ok=True)
    pdf_filename = os.path.join("outputs", "report.pdf")

    try:
        doc = SimpleDocTemplate(
            pdf_filename,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'DocTitle', parent=styles['Heading1'], fontSize=20, leading=24,
            textColor=colors.HexColor('#1E293B'), spaceAfter=12
        )
        h2_style = ParagraphStyle(
            'SectionHeader', parent=styles['Heading2'], fontSize=14, leading=18,
            textColor=colors.HexColor('#0F172A'), spaceBefore=12, spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyDark', parent=styles['BodyText'], fontSize=10, leading=14,
            textColor=colors.HexColor('#334155'), spaceAfter=8
        )

        story = []
        for line in report_md.split("\n"):
            stripped = line.strip()
            if not stripped:
                story.append(Spacer(1, 6))
            elif stripped.startswith("# "):
                clean_text = stripped.replace("# ", "").strip()
                story.append(Paragraph(f"{clean_text}", title_style))
            elif stripped.startswith("## ") or stripped.startswith("### "):
                clean_text = stripped.replace("## ", "").replace("### ", "").strip()
                story.append(Paragraph(f"{clean_text}", h2_style))
            else:
                formatted = stripped.replace("**", "").replace("**", "")
                story.append(Paragraph(formatted, body_style))

        doc.build(story)
        print(f"PDF document successfully created at: {pdf_filename}")

        # Save completed execution state into SQLite memory
        save_research_run(state)

        return {"pdf_path": pdf_filename}

    except Exception as e:
        print(f"[EXPORTER ERROR] Failed generating PDF: {e}")
        return {"pdf_path": ""}