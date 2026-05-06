"""Build the NeuroTwin demo explanation PDF.

Run:
    python scripts/build_demo_submission_pdf.py

Outputs:
    artifacts/demo/demo_submission.pdf
    application_materials/output/pdf/NeuroTwin_Demo_Submission.pdf
"""

from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT
DIST = PROJECT / "artifacts" / "demo"
TMP = PROJECT / "tmp" / "pdfs"
OUTPUT_PDF = PROJECT / "application_materials" / "output" / "pdf" / "NeuroTwin_Demo说明.pdf"
OUTPUT_PDF_ASCII = PROJECT / "application_materials" / "output" / "pdf" / "NeuroTwin_Demo_Submission.pdf"
DIST_PDF = DIST / "demo_submission.pdf"
SHOT_TOP = TMP / "neurotwin_demo_top.png"
SHOT_PERTURB_TRACE = TMP / "neurotwin_demo_perturb_trace.png"
SHOT_SIGNAL_FOLDED = TMP / "neurotwin_demo_signal_folded.png"

BLUE = colors.HexColor("#2F5E9E")
GREEN = colors.HexColor("#0F7C68")
AMBER = colors.HexColor("#9A5B12")
PURPLE = colors.HexColor("#5D5A99")
INK = colors.HexColor("#17202A")
MUTED = colors.HexColor("#64707D")
LINE = colors.HexColor("#DCE2E8")
PANEL = colors.HexColor("#F8FAFC")
HEADER_BG = colors.HexColor("#F3F5F7")
LIGHT_BLUE = colors.HexColor("#EDF4FB")
LIGHT_GREEN = colors.HexColor("#EDF8F4")
LIGHT_PURPLE = colors.HexColor("#F3F1FA")
LIGHT_AMBER = colors.HexColor("#FBF5EC")


def register_fonts() -> tuple[str, str, str]:
    songti_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
    times_path = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
    times_bold_path = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
    pdfmetrics.registerFont(TTFont("SongtiSC", songti_path, subfontIndex=6))
    pdfmetrics.registerFont(TTFont("TimesNewRoman", times_path))
    pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", times_bold_path))
    return "SongtiSC", "TimesNewRoman", "TimesNewRoman-Bold"


FONT, LATIN_FONT, LATIN_BOLD = register_fonts()


ASCII_RE = re.compile(r"(?<![A-Za-z0-9_./:+#%-])([A-Za-z0-9][A-Za-z0-9_./:+#%\\-]*)(?![A-Za-z0-9_./:+#%-])")


def fontify(text: str, bold: bool = False) -> str:
    """Escape text and render Latin letters/numbers in Times New Roman."""
    latin = LATIN_BOLD if bold else LATIN_FONT
    lines = escape(text).split("\n")
    return "<br/>".join(
        ASCII_RE.sub(lambda m: f'<font name="{latin}">{m.group(1)}</font>', line)
        for line in lines
    )


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName=FONT,
            fontSize=27,
            leading=33,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName=FONT,
            fontSize=11.5,
            leading=17,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=12,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName=FONT,
            fontSize=16.2,
            leading=22,
            textColor=INK,
            spaceBefore=5,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName=FONT,
            fontSize=11.8,
            leading=17,
            textColor=BLUE,
            spaceBefore=6,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=9.1,
            leading=13.9,
            textColor=INK,
            spaceAfter=5,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7.9,
            leading=11.2,
            textColor=MUTED,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "table": ParagraphStyle(
            "table",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7.45,
            leading=10.2,
            textColor=INK,
            wordWrap="CJK",
        ),
        "table_header": ParagraphStyle(
            "table_header",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=7.65,
            leading=10.4,
            textColor=INK,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName=LATIN_FONT,
            fontSize=6.8,
            leading=8.6,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#F1F5F9"),
            leftIndent=5,
            rightIndent=5,
            spaceBefore=3,
            spaceAfter=5,
        ),
    }


S = styles()


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(fontify(text), S[style])


def pb(text: str, style: str = "body") -> Paragraph:
    return Paragraph(fontify(text, bold=True), S[style])


def code(text: str) -> Preformatted:
    return Preformatted(text.strip("\n"), S["code"])


def bullet(items: list[str]) -> ListFlowable:
    rows = [[p("• " + item, "body")] for item in items]
    table = Table(rows, colWidths=[165 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    return table


def make_table(rows: list[list[str]], col_widths: list[float], header: bool = True) -> Table:
    data = []
    for row_index, row in enumerate(rows):
        style = "table_header" if header and row_index == 0 else "table"
        data.append([pb(cell, style) if header and row_index == 0 else p(cell, style) for cell in row])
    table = Table(data, colWidths=col_widths, hAlign="LEFT")
    table_style = [
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 1 if header else 0), (-1, -1), colors.white),
    ]
    if header:
        table_style.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor("#AAB4BF")),
            ]
        )
    table.setStyle(TableStyle(table_style))
    return table


def callout(title: str, body: str, color: colors.Color = BLUE) -> Table:
    table = Table([[pb(title, "table_header")], [p(body, "table")]], colWidths=[165 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), HEADER_BG),
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#FBFCFD")),
                ("LINEBEFORE", (0, 0), (0, -1), 2.0, color),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def dsvl_table() -> Table:
    rows = [
        ["阶段", "科学问题", "核心计算/动作", "本轮产物", "回流到下一轮"],
        ["Design", "要验证哪个脑机制或干预目标？", "证据卡片、任务场景、目标函数、候选扰动", "scenario objective, evidence cards", "更新问题空间和候选机制"],
        ["Simulate", "surrogate brain 在任务/扰动下如何响应？", "ROI 动力学预测、FC/EC 估计、虚拟扰动", "BOLD prediction, FC shift, EC response", "暴露不确定性与候选收益"],
        ["Validate", "结果是否通过可信度门控？", "Signal fidelity、FC reproducibility、objective effect、budget、external evidence", "Validation Ledger, review gate queue", "决定 pass/watch/review/hold"],
        ["Learn", "下一轮应改变什么？", "多目标 acquisition policy、负证据记录、下一轮任务生成", "Next Validation Packet", "生成新的验证任务和策略权重"],
    ]
    return make_table(rows, [18 * mm, 39 * mm, 44 * mm, 32 * mm, 32 * mm])


def dsvl_loop_diagram() -> Table:
    labels = [
        ("1 Design", "hypothesis<br/>objective<br/>evidence cards", LIGHT_BLUE),
        ("2 Simulate", "surrogate brain<br/>virtual perturbation<br/>FC/EC response", LIGHT_GREEN),
        ("3 Validate", "ledger gates<br/>review queue<br/>public protocol", LIGHT_PURPLE),
        ("4 Learn", "acquisition policy<br/>negative evidence<br/>next packet", LIGHT_AMBER),
    ]
    row = [p(f"{title}\n{body.replace('<br/>', '\n')}", "table") for title, body, _ in labels]
    loop_note = [
        p(
            "Loop: Design feeds Simulate; Simulate feeds Validate; Validate feeds Learn; Learn writes the next Design packet.",
            "small",
        )
    ]
    table = Table([row, loop_note], colWidths=[40 * mm] * 4, hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, 0), 0.6, LINE),
                ("SPAN", (0, 1), (-1, 1)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("ALIGN", (0, 1), (-1, 1), "LEFT"),
                ("LEFTPADDING", (0, 0), (-1, 0), 5),
                ("RIGHTPADDING", (0, 0), (-1, 0), 5),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, 1), 5),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 5),
                ("BACKGROUND", (0, 0), (0, 0), labels[0][2]),
                ("BACKGROUND", (1, 0), (1, 0), labels[1][2]),
                ("BACKGROUND", (2, 0), (2, 0), labels[2][2]),
                ("BACKGROUND", (3, 0), (3, 0), labels[3][2]),
            ]
        )
    )
    return table


def image_block(path: Path, caption: str, max_width: float = 165 * mm, max_height: float = 98 * mm) -> list:
    if not path.exists():
        return [callout("截图缺失", f"未找到 {path}。请先用 Playwright 生成 Demo 截图。", AMBER)]
    img = Image(str(path))
    scale = min(max_width / img.imageWidth, max_height / img.imageHeight)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    return [img, Spacer(1, 2 * mm), p(caption, "small")]


def cover() -> list:
    return [
        Spacer(1, 3 * mm),
        p("NeuroTwin Demo 说明", "title"),
        p("面向神经系统研发的 Surrogate Brain 可迭代科学闭环", "subtitle"),
        p(
            "NeuroTwin 做的是：把 ROI 级 fMRI-like 信号、脑科学假设、候选扰动和验证指标封装成一个可运行的 surrogate brain 工作流。输入是任务场景、证据卡片和脑区时间序列；输出是虚拟扰动响应、验证台账、下一轮验证包和可交给 Agent 调度的工件。本 PDF 可作为 Demo 说明直接提交，包含核心思路、技术路径、截图、关键代码、数据材料和脱敏边界。",
        ),
        callout(
            "价值与意义",
            "项目的核心价值是把复杂脑科学问题抽象成 AI4S 可调度对象：问题被拆成 Design、Simulate、Validate、Learn 四段，每段都有输入、计算动作、输出文件、可信度门控和回流路径。这样可以在真实实验前进行低成本 dry-run，保留失败或弱结果作为 negative evidence，并让下一轮实验选择由数据、证据和策略共同决定。",
            GREEN,
        ),
        Spacer(1, 4 * mm),
        dsvl_loop_diagram(),
        Spacer(1, 4 * mm),
        make_table(
            [
                ["问题", "NeuroTwin 的回答", "对应工件"],
                ["究竟在做什么？", "把脑影像分析从单次建模推进到可运行的虚拟实验闭环：先设计可检验假设，再用 surrogate brain 模拟扰动，随后进入验证门控，最后生成下一轮任务。", "brain_twin_lab.html, demo_data.json"],
                ["如何体现 AI4S？", "它把科学问题拆成 workflow：证据输入、数据准备、模型仿真、可信验证、策略学习和交接包生成。每一步都能被记录、复查、替换和自动调度。", "agent_skill_registry.md, experiment_trace.jsonl"],
                ["为什么有价值？", "在真实 fMRI、神经调控或药物机制验证前，先用可审计虚拟实验筛选假设、暴露不确定性、生成公开验证协议，减少盲目实验成本。", "validation_ledger.md, public_validation_manifest.json"],
                ["如何持续迭代？", "Validate 产生 pass/watch/review/hold 状态；Learn 把指标快照、负证据和下一步策略写入 packet，下一轮 Design 直接读取。", "next_validation_packet.json"],
            ],
            [31 * mm, 93 * mm, 41 * mm],
        ),
        Spacer(1, 4 * mm),
        make_table(
            [
                ["层面", "已经实现", "还没有实现", "希望实现与 Scaling 路线"],
                ["数据", "合成脱敏 ROI 级 fMRI-like 数据、公开数据验证模板。", "尚未接入真实受试者影像或行为读数。", "先做 OpenNeuro P1 smoke test，再扩展到 HCP/ABCD、多任务、多站点。"],
                ["模型", "轻量一步预测 surrogate、FC/EC 与虚拟扰动响应。", "尚未训练大规模 subject-aware 或 task-aware 模型。", "扩展为图时序模型、个体化模型和多模态脑表型基础模型。"],
                ["闭环", "Validation Ledger、Review Queue、Next Validation Packet 已生成。", "尚未接入真实实验室执行和人类专家签核系统。", "把每轮 packet 变成 Agent 可执行任务，支持持续实验队列和学习记忆。"],
                ["平台化", "Read/Prepare/Build/Compute/Validate/Learn 技能路线已定义。", "尚未接入 Bohrium/SciMaster/实验操作系统。", "按统一 schema 暴露为 AI4S workflow 节点，支持数据集、任务和模型规模扩展。"],
            ],
            [23 * mm, 45 * mm, 43 * mm, 54 * mm],
        ),
        Spacer(1, 3 * mm),
        p("建议阅读顺序：第 2 页看 DSVL 机制，第 3-5 页看 Demo 截图，第 6 页看关键代码，第 7 页看提交材料和边界。", "small"),
    ]


def page_dsvl() -> list:
    return [
        p("一、DSVL 是 NeuroTwin 的核心", "h1"),
        p(
            "NeuroTwin 的重点是展示一个可以持续迭代的科学闭环。它把脑科学问题拆成四个可审计阶段，并让每个阶段都有明确输入、计算动作、输出文件和下一轮回流对象。",
        ),
        dsvl_table(),
        Spacer(1, 6 * mm),
        p("闭环对象如何流动", "h2"),
        make_table(
            [
                ["对象", "生成阶段", "用途", "进入下一轮的方式"],
                ["Evidence Cards", "Design", "把文献、标准和方法建议转成结构化假设输入", "影响目标函数、ROI 选择和验证指标"],
                ["Virtual Perturbation Response", "Simulate", "在真实实验前测试候选机制的网络级影响", "暴露收益、风险和不确定性"],
                ["Validation Ledger", "Validate", "把模型输出拆成可复核门控", "review/watch 进入下一轮验证任务"],
                ["Acquisition Portfolio", "Learn", "排序下一轮候选实验", "更新实验优先级和策略权重"],
                ["Next Validation Packet", "Learn", "把本轮结果打包成机器可读任务", "作为下一轮 Design 输入"],
            ],
            [33 * mm, 24 * mm, 56 * mm, 52 * mm],
        ),
        Spacer(1, 5 * mm),
        callout(
            "关键判断",
            "如果只保留一个创新点，NeuroTwin 的价值在于把 surrogate brain 变成可运行、可验证、可回流的 AI4S 实验循环；DSVL 是这个循环的任务语言和工件协议。",
            GREEN,
        ),
    ]


def page_demo_top() -> list:
    return [
        p("二、Demo 示例：核心 AI4S Workflow 首屏", "h1"),
        p(
            "第一张图展示 Demo 的进入方式：顶部先说明 Core idea 与 Demo proof，随后用场景切换、关键指标和 AI4S Platform Route 告诉评审系统在做什么。这里的重点是把脑科学问题放入一个平台化 workflow：知识输入和数据准备进入 NeuroTwin virtual world，仿真结果进入 validation gates，再由 acquisition policy 生成下一轮实验和 learning memory。",
        ),
        *image_block(
            SHOT_TOP,
            "图 1：核心 workflow 首屏。它直观展示 NeuroTwin 如何把 Design、Simulate、Validate、Learn 放在同一个可调度 AI4S 平台路线中。",
            max_height=124 * mm,
        ),
    ]


def page_demo_perturb_trace() -> list:
    return [
        p("三、Demo 示例：Virtual Perturbation Map 与 DSVL Trace", "h1"),
        p(
            "第二张图展示核心技术路径：左侧是 surrogate brain 上的虚拟扰动响应，右侧是 DSVL Trace。评审可以看到：虚拟扰动会被记录为 Design、Simulate、Validate、Learn 四个阶段的可审计任务链，每一步都有状态和产物。",
        ),
        *image_block(
            SHOT_PERTURB_TRACE,
            "图 2：虚拟扰动图与 DSVL Trace。左侧说明候选扰动如何影响脑网络，右侧说明该结果如何进入可复现、可验证、可回流的科学闭环。",
            max_height=124 * mm,
        ),
    ]


def page_demo_signal_folded() -> list:
    return [
        p("四、Demo 示例：Signal Simulation 与折叠式证据区", "h1"),
        p(
            "第三张图展示 Demo 的可读性改造：Signal Simulation 和 Candidate Policy 保持展开，用于证明 surrogate 运行结果和候选策略；Validation gates、Workflow/Agent implementation details、Evidence and submission artifacts 被折叠起来，评审需要查看可行性证据时再展开。这样页面优先聚焦项目核心思路、初步落地构想和关键技术路径。",
        ),
        *image_block(
            SHOT_SIGNAL_FOLDED,
            "图 3：信号仿真、候选策略和折叠式证据区。核心结果留在主视图，验证台账、Agent 路由和提交材料作为可展开证据保留。",
            max_height=124 * mm,
        ),
    ]


def page_code() -> list:
    return [
        p("五、关键代码如何证明闭环可执行", "h1"),
        p("提交包中包含完整代码。PDF 摘录最关键的三段，说明 DSVL 已经落在可运行对象、门控规则和交接包里。"),
        p("1. Surrogate Brain：ROI 时间序列到一步预测模型", "h2"),
        code(
            """
# src/neurotwin/core.py
def fit_surrogate(series, alpha=0.65):
    x_prev = series[:-1]
    y_next = series[1:]
    x_aug = concatenate([x_prev, ones_bias], axis=1)
    coef = solve(x_aug.T @ x_aug + ridge_reg, x_aug.T @ y_next)
    return coef

def effective_connectivity_from_surrogate(series, coef, delta=0.30):
    # perturb each source node and average one-step response
    return virtual_effective_connectivity
            """
        ),
        p("2. Validate：每轮输出进入可信度台账", "h2"),
        code(
            """
# scripts/run_demo.py
def build_validation_ledger(metrics, learning):
    gates = [
        gate("Signal fidelity", metrics["bold_r2"], pass_at=0.70),
        gate("FC reproducibility", metrics["fc_corr"], pass_at=0.75),
        gate("Objective effect", abs(metrics["objective_delta"]), pass_at=0.08),
        gate("Perturbation budget", intervention_cost, pass_at=0.55),
        {"gate": "External evidence", "status": "review"},
    ]
    return {
        "gates": gates,
        "review_queue": build_public_review_queue(),
        "escalation_rule": "watch/review gates create validation tasks"
    }
            """
        ),
        p("3. Learn：本轮结果被打包为下一轮验证任务", "h2"),
        code(
            """
# scripts/run_demo.py
next_validation_packet = {
    "scenario": scenario_key,
    "objective": scenario.objective,
    "linked_evidence_cards": evidence_cards,
    "current_metric_snapshot": metrics,
    "learn_stage_action": top_acquisition_action,
    "negative_evidence": low_priority_actions,
    "decision_rule": "advance only when gates and protocol are satisfied"
}
write_json("artifacts/demo/next_validation_packet.json", next_validation_packet)
            """
        ),
    ]


def page_materials() -> list:
    return [
        p("六、提交材料、运行方式与边界", "h1"),
        p("推荐提交材料位于 application_materials/output/。PDF、网页、数据与核心代码均可由脚本重新生成。"),
        make_table(
            [
                ["类别", "文件", "证明内容"],
                ["说明文档", "docs/demo/ / artifacts/demo/demo_submission.pdf", "项目目标、DSVL 闭环、Demo 展示方式、能力边界"],
                ["核心代码", "src/neurotwin/core.py", "合成 ROI 信号、surrogate dynamics、FC/EC 与扰动响应"],
                ["核心代码", "scripts/run_demo.py", "生成 Demo 网页、指标、Validation Ledger、Agent route、Next Validation Packet"],
                ["核心代码", "scripts/prepare_public_validation.py", "把 review gate 转成公开 fMRI 验证 manifest、runbook 和 protocol template"],
                ["数据产物", "artifacts/demo/demo_data.json", "脱敏合成数据、模型指标、验证台账、DSVL 对象"],
                ["交互 Demo", "artifacts/demo/brain_twin_lab.html", "可视化展示 DSVL、虚拟扰动、验证门控和 Learn 阶段策略"],
                ["验证包", "artifacts/demo/next_validation_packet.json", "本轮结果到下一轮任务的机器可读交接对象"],
            ],
            [25 * mm, 55 * mm, 85 * mm],
        ),
        Spacer(1, 5 * mm),
        p("运行命令", "h2"),
        code(
            """
python scripts/run_demo.py
python scripts/prepare_public_validation.py
python scripts/prepare_public_validation.py --scenario emotion --tier 1 \\
  --output-prefix public_validation_openneuro_smoke
python -m http.server 8771 --directory artifacts/demo
            """
        ),
        p("脱敏与能力边界", "h2"),
        bullet(
            [
                "当前 Demo 使用合成 ROI 级 fMRI-like 数据，由代码中的稳定非线性动力学系统生成。",
                "提交包不包含真实受试者 MRI、DICOM、NIfTI、面部图像、姓名、身份证件、联系方式、住院号、设备原始记录或临床诊断信息。",
                "公开数据相关文件只包含 OpenNeuro/HCP/ABCD 的验证路线、协议模板和工具清单，未下载或再分发真实受试者数据。",
                "当前结果用于证明项目思路、技术路径和可迭代闭环，不用于临床诊断或真实治疗效果预测。",
            ]
        ),
        Spacer(1, 4 * mm),
        callout(
            "展示建议",
            "3-5 分钟演示时按 DSVL 讲：Design 看 evidence cards 与任务目标；Simulate 看虚拟扰动图和信号预测；Validate 看 ledger 与 review queue；Learn 看 acquisition policy 与 next validation packet。",
            BLUE,
        ),
    ]


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(MUTED)
    x = 20 * mm
    canvas.setFont(LATIN_FONT, 8)
    canvas.drawString(x, 12 * mm, "NeuroTwin Demo")
    x += pdfmetrics.stringWidth("NeuroTwin Demo", LATIN_FONT, 8) + 2
    canvas.setFont(FONT, 8)
    canvas.drawString(x, 12 * mm, "说明")
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
        title="NeuroTwin Demo 说明",
        author="NeuroTwin",
    )
    story = []
    for page in [cover, page_dsvl, page_demo_top, page_demo_perturb_trace, page_demo_signal_folded, page_code, page_materials]:
        if story:
            story.append(PageBreak())
        story.extend(page())
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    build_pdf(DIST_PDF)
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DIST_PDF, OUTPUT_PDF)
    shutil.copyfile(DIST_PDF, OUTPUT_PDF_ASCII)
    print(f"Wrote {DIST_PDF}")
    print(f"Wrote {OUTPUT_PDF}")
    print(f"Wrote {OUTPUT_PDF_ASCII}")


if __name__ == "__main__":
    main()
