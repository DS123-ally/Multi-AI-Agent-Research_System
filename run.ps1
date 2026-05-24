Set-Location $PSScriptRoot
& "$PSScriptRoot\venv\Scripts\Activate.ps1"
python -m streamlit run app.py
