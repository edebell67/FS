import os
import pandas as pd
import glob

def generate_consolidated_report():
    base_epic_path = r"C:\Users\edebe\eds\epics\ep_014_website_break_fix"
    owners_path = os.path.join(base_epic_path, "owners")
    report_output_path = os.path.join(base_epic_path, "Website_Break_Fix_Report.xlsx")
    
    all_data = []
    
    # Iterate through all owner folders
    for owner_dir in os.listdir(owners_path):
        owner_full_path = os.path.join(owners_path, owner_dir)
        if os.path.isdir(owner_full_path):
            report_file = os.path.join(owner_full_path, "broken_links_report.txt")
            if os.path.exists(report_file):
                with open(report_file, 'r') as f:
                    lines = f.readlines()
                    target_url = ""
                    for line in lines:
                        if line.startswith("Target URL:"):
                            target_url = line.split("Target URL:")[1].strip()
                        if line.startswith("URL:"):
                            # Parse: URL: http://... | Status: 404
                            parts = line.split("|")
                            broken_url = parts[0].replace("URL:", "").strip()
                            status = parts[1].replace("Status:", "").strip()
                            
                            all_data.append({
                                'Owner': owner_dir,
                                'Website': target_url,
                                'Broken Link': broken_url,
                                'Status Code': status,
                                'Artifacts Folder': owner_full_path
                            })
            else:
                # Check for critical failures (like dew_beauty)
                all_data.append({
                    'Owner': owner_dir,
                    'Website': 'N/A (Check Logs)',
                    'Broken Link': 'CRITICAL SITE FAILURE',
                    'Status Code': 'FAIL',
                    'Artifacts Folder': owner_full_path
                })

    if all_data:
        df = pd.DataFrame(all_data)
        # Reorder columns
        df = df[['Owner', 'Website', 'Broken Link', 'Status Code', 'Artifacts Folder']]
        
        # Save to Excel
        df.to_excel(report_output_path, index=False)
        print(f"Consolidated Excel report generated at: {report_output_path}")
    else:
        print("No data found to generate report.")

if __name__ == "__main__":
    generate_consolidated_report()
