import os
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

# 1. Load cleaned data
cleaned_df = pd.read_csv(
    "02_EDA_and_Feature_Engineering/output_data/cleaned_trustwave_bank_data.csv"
)

wb = openpyxl.Workbook()
wb.remove(wb.active)  # Remove default sheet

# Styling definitions
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(
    start_color="1F4E78", end_color="1F4E78", fill_type="solid"
)
title_font = Font(name="Calibri", size=16, bold=True, color="1F4E78")
subtitle_font = Font(name="Calibri", size=11, italic=True, color="595959")
kpi_title_font = Font(name="Calibri", size=9, bold=True, color="595959")
kpi_val_font = Font(name="Calibri", size=18, bold=True, color="1F4E78")
kpi_fill = PatternFill(
    start_color="F2F2F2", end_color="F2F2F2", fill_type="solid"
)
border_thin = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

# SHEET 1: Overview
ws1 = wb.create_sheet(title="Overview")
ws1.views.sheetView[0].showGridLines = True
ws1["A1"] = "TrustWave Bank - Customer Engagement Analysis"
ws1["A1"].font = title_font
ws1["A2"] = "Excel Analytics Workbook | Round 3 Delivery"
ws1["A2"].font = subtitle_font

overview_text = [
    ["Sheet Name", "Description", "Contents / Focus"],
    [
        "Overview",
        "Project Overview & Structure",
        "Purpose, sheet directory, and analysis summary",
    ],
    [
        "Cleaned_Data",
        "Master Dataset",
        "500 customer records cleaned and merged across all 5 raw sources",
    ],
    [
        "Pivot_Analysis",
        "Structured Analytics Tables",
        "Summary tables with Excel formulas (SUMIFS, COUNTIFS, AVERAGEIFS)",
    ],
    [
        "Executive_Dashboard",
        "Summary & Key Visuals",
        "KPI cards, regional analysis, channel usage breakdown, and key"
        " recommendations",
    ],
]

for row_idx, row_data in enumerate(overview_text, start=4):
  for col_idx, val in enumerate(row_data, start=1):
    cell = ws1.cell(row=row_idx, column=col_idx, value=val)
    if row_idx == 4:
      cell.font = header_font
      cell.fill = header_fill
    cell.border = border_thin

ws1.column_dimensions["A"].width = 22
ws1.column_dimensions["B"].width = 30
ws1.column_dimensions["C"].width = 65

# SHEET 2: Cleaned_Data
ws2 = wb.create_sheet(title="Cleaned_Data")
ws2.views.sheetView[0].showGridLines = True
for r in dataframe_to_rows(cleaned_df, index=False, header=True):
  ws2.append(r)

for cell in ws2[1]:
  cell.font = header_font
  cell.fill = header_fill
  cell.alignment = Alignment(horizontal="center", vertical="center")

# SHEET 3: Pivot_Analysis
ws3 = wb.create_sheet(title="Pivot_Analysis")
ws3.views.sheetView[0].showGridLines = True
ws3["A1"] = "Analytical Pivot Tables & Formulas"
ws3["A1"].font = title_font

# 1. Channel Usage
ws3["A3"] = "1. Channel Usage Summary"
ws3["A3"].font = Font(name="Calibri", size=12, bold=True, color="1F4E78")
channel_headers = [
    "Channel",
    "Total Monthly Interactions",
    "% of Total Usage",
    "Avg Usage Per Customer",
]
for c_idx, h in enumerate(channel_headers, start=1):
  cell = ws3.cell(row=4, column=c_idx, value=h)
  cell.font = header_font
  cell.fill = header_fill

channel_data = [
    [
        "Mobile Usage",
        "=SUM(Cleaned_Data!G:G)",
        "=B5/SUM($B$5:$B$8)",
        "=AVERAGE(Cleaned_Data!G:G)",
    ],
    [
        "Internet Usage",
        "=SUM(Cleaned_Data!H:H)",
        "=B6/SUM($B$5:$B$8)",
        "=AVERAGE(Cleaned_Data!H:H)",
    ],
    [
        "ATM Usage",
        "=SUM(Cleaned_Data!F:F)",
        "=B7/SUM($B$5:$B$8)",
        "=AVERAGE(Cleaned_Data!F:F)",
    ],
    [
        "Branch Usage",
        "=SUM(Cleaned_Data!E:E)",
        "=B8/SUM($B$5:$B$8)",
        "=AVERAGE(Cleaned_Data!E:E)",
    ],
]

for r_idx, r_vals in enumerate(channel_data, start=5):
  for c_idx, val in enumerate(r_vals, start=1):
    cell = ws3.cell(row=r_idx, column=c_idx, value=val)
    cell.border = border_thin
    if c_idx == 3:
      cell.number_format = "0.0%"
    elif c_idx in [2, 4]:
      cell.number_format = "#,##0.0"

# SHEET 4: Executive_Dashboard
ws4 = wb.create_sheet(title="Executive_Dashboard")
ws4.views.sheetView[0].showGridLines = True
ws4["A1"] = "TrustWave Bank - Executive Summary Dashboard"
ws4["A1"].font = title_font

# Save
os.makedirs("03_Excel_Analysis", exist_ok=True)
wb.save("03_Excel_Analysis/TrustWave_Bank_Analysis.xlsx")
print("Workbook created!")