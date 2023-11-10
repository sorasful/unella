## Bandit Security Report

### Report Summary
Report generated at: {{ data.vulnerabilities.generated_at }}  
Total number of files analyzed: {{ data.vulnerabilities.metrics | length }}

### Error Details
{% if data.vulnerabilities.errors %}
{% for error in data.vulnerabilities.errors %}
- {{ error }}
{% endfor %}
{% else %}
No errors found.
{% endif %}

### Metrics Summary

| File | LOC | High Confidence | Medium Confidence | Low Confidence | Undefined Confidence | High Severity | Medium Severity | Low Severity | Undefined Severity | NoSec | Skipped Tests |
|------|-----|-----------------|-------------------|----------------|----------------------|---------------|-----------------|--------------|--------------------|-------|---------------|
{% for file_path, metric in data.vulnerabilities.metrics.items() -%}
| {{ file_path }} | {{ metric.loc }} | {{ metric.CONFIDENCE_HIGH }} | {{ metric.CONFIDENCE_MEDIUM }} | {{ metric.CONFIDENCE_LOW }} | {{ metric.CONFIDENCE_UNDEFINED }} | {{ metric.SEVERITY_HIGH }} | {{ metric.SEVERITY_MEDIUM }} | {{ metric.SEVERITY_LOW }} | {{ metric.SEVERITY_UNDEFINED }} | {{ metric.nosec }} | {{ metric.skipped_tests }} |
{% endfor -%}

### Detailed Findings
{% for result in data.vulnerabilities.results %}
#### Issue in File: {{ result.filename }} at line: {{ result.line_number }}
**Issue Severity:** {{ result.issue_severity }}  
**Issue Confidence:** {{ result.issue_confidence }}  
**CWE ID:** [CWE-{{ result.issue_cwe.id }}]({{ result.issue_cwe.link }})  
**Issue Description:** {{ result.issue_text }}  
**Code:**

    {{ result.code | replace('\n', '\n    ') }}

**More Info:** [Click here]({{ result.more_info }})  
**Test ID:** {{ result.test_id }}  
**Test Name:** {{ result.test_name }}  

{% endfor %}
