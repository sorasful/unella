# Unella: Automatic Audit for Python Projects
Unella is a project to automate audits exclusively on Python projects.

## 🚧 Project Status
Please note that Unella is currently in active development.  
While it is functional, expect regular updates and enhancements.  

## 📄 Output Formats
With Unella, you can generate audit results in two formats:  

JSON: Structured data that can be easily consumed by other applications.  
HTML Report: A comprehensive, visual report detailing the audit findings.  
Markdown Report: Same as HTML but in markdown..  

## 🛠️ Tools Integrated
Unella is powered by a suite of reputable Python tools to offer a diverse range of insights:

Ruff: https://github.com/astral-sh/ruff  
Mypy: https://github.com/python/mypy  
vulture: https://github.com/jendrikseipp/vulture  
Radon: https://github.com/rubik/radon  
Gitleaks: https://github.com/gitleaks/gitleaks  
Bandit: https://github.com/PyCQA/bandit  

...and several other tools to fetch a plethora of information.  

## 💼 Installation & Usage
Use the Unella Command-Line Interface (CLI) to start your audit through Docker:  
We need to mount the directory we want to analyze to `/path`.  
We need to mount our current directory to store the results there for HTML and JSON reports.  

### From Docker hub
```bash
docker build -t unella .
docker run -v /home/tevak/dev/jwt_tool:/path -v "$PWD/results:/opt/unella/results"  -it unella  --path /path
```

For example if you want to get JSON as stdout
```bash
docker run -v /home/tevak/dev/jwt_tool:/path -v "$PWD/results:/opt/unella/results"  -it unella  --path /path --output-format json
```

If you want to generate a HTML report you'll need to mount a directory to get results
```bash
docker run -v /home/tevak/dev/jwt_tool:/path -v "$PWD/results:/opt/unella/results"  -it unella  --path /path --output-format html
```


Replace path_to_python_project with the path to your Python project.  
For an HTML report, replace json with html.
