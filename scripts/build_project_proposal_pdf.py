"""Build the NeuroTwin project proposal PDF.

Run:
    python scripts/build_project_proposal_pdf.py

Outputs:
    artifacts/demo/project_proposal.pdf
    application_materials/output/pdf/NeuroTwin_Project_Proposal.pdf
    application_materials/output/pdf/NeuroTwin_项目提议.pdf
"""

from __future__ import annotations

import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer, Table, TableStyle

from build_demo_submission_pdf import (
    BLUE,
    FONT,
    GREEN,
    HEADER_BG,
    INK,
    LATIN_FONT,
    LINE,
    MUTED,
    callout,
    code,
    make_table,
    p,
    pb,
    pdfmetrics,
)


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT
DIST = PROJECT / "artifacts" / "demo"
DIST_PDF = DIST / "project_proposal.pdf"
OUTPUT_PDF = PROJECT / "application_materials" / "output" / "pdf" / "NeuroTwin_Project_Proposal.pdf"
OUTPUT_PDF_CN = PROJECT / "application_materials" / "output" / "pdf" / "NeuroTwin_项目提议.pdf"


PROPOSAL_SECTIONS = [
    (
        "具体目标",
        "解决神经影像分析难以从相关性描述走向可测试干预假设的问题。产出 NeuroTwin：把 ROI 级 fMRI 信号、证据卡、任务目标和候选扰动封装为可运行 surrogate brain workflow，输出虚拟扰动响应、信号仿真、Validation Ledger、Next Validation Packet 和 Agent 接口。",
    ),
    (
        "核心价值",
        "NeuroTwin 将复杂脑科学问题抽象为 DSVL 闭环，使真实实验前可以低成本 dry-run、暴露不确定性、记录负证据并生成下一轮建议。它补齐分子、蛋白、基因模型到脑功能表型之间的系统级仿真层，把神经系统研发转为可复用、可验证、可扩展的 AI4S workflow。",
    ),
    (
        "可行性简析",
        "关键路径：公开或合成 fMRI 到 ROI 时间序列，再到 surrogate dynamics、虚拟扰动、验证门控和下一轮验证包。资源包括 OpenNeuro/HCP/ABCD、BIDS/fMRIPrep、atlas、基础算力和专家审阅。风险是噪声高、泛化弱、解释过强；用 BOLD R2、FC 一致性、扰动稳定性、subject split、跨数据集复现和人工 gate 验证。",
    ),
]


def proposal_matrix() -> Table:
    return make_table(
        [
            ["要求", "项目提议中的回答"],
            ["要解决什么问题", "神经影像结果难以从相关性描述走向可测试、可迭代的干预假设。"],
            ["产出是什么", "Surrogate brain workflow、虚拟扰动响应、信号仿真、验证台账、下一轮验证包和 Agent 接口。"],
            ["为什么值得做", "让神经系统研发具备低成本 dry-run、可审计验证、负证据回流和跨层级表型仿真能力。"],
            ["如何验证", "BOLD R2、FC 一致性、扰动稳定性、subject split、跨数据集复现和人工 review gate。"],
        ],
        [36 * mm, 129 * mm],
    )


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(MUTED)
    x = 20 * mm
    canvas.setFont(LATIN_FONT, 8)
    canvas.drawString(x, 12 * mm, "NeuroTwin Project Proposal")
    canvas.setFont(LATIN_FONT, 8)
    canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=17 * mm,
        title="NeuroTwin 项目提议",
        author="NeuroTwin",
    )
    story = [
        Spacer(1, 10 * mm),
        p("NeuroTwin 项目提议", "title"),
        p("面向神经系统研发的 Surrogate Brain 可迭代科学闭环", "subtitle"),
        callout(
            "项目名称",
            "NeuroTwin：面向神经系统研发的 Surrogate Brain 可迭代科学闭环",
            BLUE,
        ),
        Spacer(1, 5 * mm),
    ]
    for title, body in PROPOSAL_SECTIONS:
        story.extend([p(title, "h1"), p(body), Spacer(1, 2 * mm)])
    story.extend(
        [
            Spacer(1, 3 * mm),
            p("提交要求对应", "h1"),
            proposal_matrix(),
            Spacer(1, 5 * mm),
            callout(
                "与 Demo 的关系",
                "Demo PDF 展示上述提议的最小可行版本：合成脱敏 ROI 信号、surrogate dynamics、虚拟扰动、DSVL Trace、Validation Ledger、Next Validation Packet 和折叠式证据区。",
                GREEN,
            ),
        ]
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    build_pdf(DIST_PDF)
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DIST_PDF, OUTPUT_PDF)
    shutil.copyfile(DIST_PDF, OUTPUT_PDF_CN)
    print(f"Wrote {DIST_PDF}")
    print(f"Wrote {OUTPUT_PDF}")
    print(f"Wrote {OUTPUT_PDF_CN}")


if __name__ == "__main__":
    main()
