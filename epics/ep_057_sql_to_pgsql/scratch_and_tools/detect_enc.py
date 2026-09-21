for enc in ['utf-8', 'utf-8-sig', 'cp1252', 'latin1', 'utf-16le', 'utf-16']:
    try:
        with open(r"C:\Users\edebe\eds\db_scripts\dbo.sp_001_create_trades_brk.StoredProcedure.sql", "r", encoding=enc) as f:
            text = f.read()
        print(f"Successfully read with {enc}, length: {len(text)}")
        with open(r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\sp_001_brk_raw.txt", "w", encoding="utf-8") as f_out:
            f_out.write(text.lstrip('\ufeff'))
        break
    except Exception as e:
        print(f"Failed {enc}: {e}")
