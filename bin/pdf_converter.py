import pdfplumber
import json
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")


def extract_pdf_to_dict(pdf_path, hallticket_column_name="Hall_Ticket_Number"):
    result_dict = {}
    headers = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(page_num)
            table = page.extract_table()
            # print(table)
            if not table:
                print(f"❌ No table found on page {page_num + 1}")
                continue
            
            for row in table:
                # print("row ", row)
                if not headers and page_num == 0:
                    headers = [h.strip().replace("\n", "_").replace(" ", "_") for h in table[0]]
                    headers[0] = 'Hall_Ticket_Number'
                    print("Headers ", headers)
                print("Len: ", len(row), " len(headers): ", len(headers))
                # print(f"row: {row}")
                # input("ss")
                if len(row) != len(headers):
                    print(f"⚠️ Skipping row with mismatched columns on page {page_num + 1}: {row}")
                    continue

                row_dict = {header: (value.strip() if value else "") for header, value in zip(headers, row)}
                hallticket = row_dict.get(hallticket_column_name)

                if hallticket:
                    result_dict[hallticket] = row_dict
                    print(f"row_dict: {row_dict}")
                else:
                    print(f"⚠️ No hallticket in row: {row_dict}")
                    # break
                # break
            # break
    # print(f"result_dict: {result_dict}")
    return result_dict

# ✅ Run and Save
if __name__ == "__main__":
    pdf_path = "bin/input/RESULT-SHARED-DEPT-040402025_compressed.pdf"
    data_dict = extract_pdf_to_dict(pdf_path)

    print(f"✅ Extracted {len(data_dict)} entries.")
    with open(f"bin/output/results_{str(datetime.now())}.json", "w", encoding="utf-8") as f:
        json.dump(data_dict, f, indent=2, ensure_ascii=False)
