with open(r"C:\Users\edebe\eds\db_scripts\dbo.sp_003_CloseTradesTargetReached_refactored.StoredProcedure.sql", "r", encoding="utf-16le") as f:
    text = f.read()

# Strip BOM if present
text = text.lstrip('\ufeff')

lines = text.splitlines()
print(f"Total lines: {len(lines)}")

with open(r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\sp_003_raw.txt", "w", encoding="utf-8") as f_out:
    f_out.write(text)
print("Saved utf-8 version to scratch/sp_003_raw.txt")
