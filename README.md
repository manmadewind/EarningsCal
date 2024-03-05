# EarningsCal
```
name: Daily Job
on:
  schedule:
    - cron: '0 8 * * *' # 每天早上8点运行

jobs:
  run-main-py:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        pip install finance_calendars ics
    - name: Run main.py
      run: python main.py
    - name: Commit & Push Results
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git commit -m "Auto-commit daily job results"
        git push
```