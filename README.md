# ICE Robusta Coffee Certified Stocks Tracker

Automated dashboard tracking Robusta coffee certified stocks from ICE Futures Europe (Report 173).

## 📊 Dashboard Features

- **Real-time Stock Tracking**: Valid, Non-Tenderable, and Suspended lots
- **Port Breakdown**: 13 European and US delivery points (Antwerp, London, Barcelona, etc.)
- **Historical Charts**: Interactive time-series with date range filters (All / YTD / 3M / 1M)
- **Day-over-Day Changes**: Color-coded indicators for all metrics
- **Teams Integration**: Daily automated alerts with significant move detection

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/RobustaCertifiedStocks.git
cd RobustaCertifiedStocks

# Install Python dependencies
pip install requests
```

### 2. Load Historical Data (3 Years)

```bash
# Download 3 years of historical data from ICE
# This will take ~30-45 minutes due to rate limiting
python3 load_robusta_history_improved.py
```

**Important**: The script includes:
- 2-second delays between requests (critical to avoid ICE blocking)
- Exponential backoff on HTTP 429 errors
- Automatic weekend skipping (no data published)

### 3. Generate Dashboard

```bash
# Parse CSV files and inject data into HTML
python3 update_robusta_dashboard.py

# The dashboard is now ready at index.html
```

### 4. Deploy to GitHub Pages

```bash
# Create GitHub repository and push
git init
git add .
git commit -m "Initial Robusta dashboard"
git remote add origin https://github.com/YOUR_USERNAME/RobustaCertifiedStocks.git
git push -u origin main

# Enable GitHub Pages
# Go to Settings → Pages → Source: main branch → Save
```

Your dashboard will be live at: `https://YOUR_USERNAME.github.io/RobustaCertifiedStocks/`

## 🤖 Automation Setup

### Daily Updates (GitHub Actions)

1. Create workflow directory:
```bash
mkdir -p .github/workflows
cp .github_workflows_update_robusta_dashboard.yml .github/workflows/update_robusta_dashboard.yml
```

2. Commit and push:
```bash
git add .github/workflows/
git commit -m "Add daily automation workflow"
git push
```

The workflow runs automatically every business day at 15:00 UTC (after ICE publishes data).

### Teams Alerting

1. Create a Teams webhook:
   - Go to your Teams channel
   - Click ⋯ → Connectors → Incoming Webhook
   - Name it "Robusta Stocks Alert"
   - Copy the webhook URL

2. Update the script:
```bash
# Edit send_robusta_teams_alert.py
# Replace TEAMS_WEBHOOK_URL with your actual webhook URL
# Replace YOUR_GITHUB_USERNAME and YOUR_REPO_NAME with your values
```

3. Test the alert:
```bash
python3 send_robusta_teams_alert.py
```

4. Add to GitHub Actions workflow (optional):
   - Edit `.github/workflows/update_robusta_dashboard.yml`
   - Add webhook URL as GitHub secret
   - Uncomment the Teams alert step

## 📁 Project Structure

```
RobustaCertifiedStocks/
├── index.html                          # Dashboard (auto-generated)
├── robusta_index.html                  # Dashboard template
├── update_robusta_dashboard.py         # Data injection script
├── load_robusta_history_improved.py    # Historical data loader
├── send_robusta_teams_alert.py         # Teams alerting
├── Stock_Report_RC_YYYYMMDD_*.csv      # Data files (auto-downloaded)
└── .github/
    └── workflows/
        └── update_robusta_dashboard.yml # Daily automation
```

## 📖 Data Format

ICE Robusta data structure:
- **Commodity**: RC (Robusta Coffee)
- **Units**: Lots (1 lot = 10 tonnes)
- **Ports**: 13 delivery points across Europe and US
- **Categories**: Valid, Non-Tenderable, Suspended

### Port Codes
| Code | Port |
|------|------|
| ANT | Antwerp |
| LON | London |
| BAR | Barcelona |
| FEL | Felixstowe |
| AMS | Amsterdam |
| HAM | Hamburg |
| LEH | Le Havre |
| GEN | Genoa |
| BRE | Bremen |
| ROT | Rotterdam |
| TRI | Trieste |
| LIV | Liverpool |
| NOR | New Orleans |

## ⚠️ Important Notes

### Rate Limiting
- ICE blocks aggressive scraping
- Always use 2-second delays between requests
- The historical loader includes exponential backoff
- If blocked, wait 24 hours before retrying

### Data Availability
- Data published daily on business days only
- Weekends and holidays: no data
- Publication time: typically 10:00-14:00 GMT

### Critical Workflow Rule
If you manually upload a local `index.html` to GitHub, you'll **overwrite** the historical data embedded in it. 

**Correct sequence**:
1. Upload your local `index.html` to GitHub
2. Immediately run the "Load Historical Data" GitHub Action workflow
3. This re-injects the full historical dataset

## 🔧 Troubleshooting

### No data for recent dates
- ICE sometimes delays publication
- The workflow will retry automatically the next day
- Check https://www.ice.com/report/173 manually

### Dashboard not updating
- Check GitHub Actions tab for errors
- Verify CSV files are being downloaded
- Check that `update_robusta_dashboard.py` ran successfully

### Teams alerts not working
- Verify webhook URL is correct
- Test with `python3 send_robusta_teams_alert.py`
- Check Teams connector settings

## 📊 Similar Projects

- [Arabica Certified Stocks Dashboard](https://livioroth.github.io/IceCertifiedStocks/)
- ICE Coffee "C" tracking for Arabica coffee

## 📜 License

Data source: [ICE Futures Europe - Report 173](https://www.ice.com/report/173)

This project is for educational and internal business use.

## 👤 Author

**Livio Roth**  
Sucafina Trading - Tokyo Office

---

*Last updated: March 2026*
