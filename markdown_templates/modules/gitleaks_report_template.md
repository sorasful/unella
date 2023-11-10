## Gitleaks Report

### Potential Leaks Detected
Number of leaks detected: {{ data.leaks | length }}

### Leak Details
{% for leak in data.leaks %}
#### File: {{ leak.file }}

| Description | Start Line | End Line | Start Column | End Column | Match | Secret | Commit | Entropy | Author | Email | Date | Message | Rule ID | Fingerprint |
|-------------|------------|----------|--------------|------------|-------|--------|--------|---------|--------|-------|------|---------|---------|-------------|
| {{ leak.description }} | {{ leak.start_line }} | {{ leak.end_line }} | {{ leak.start_column }} | {{ leak.end_column }} | {{ leak.match }} | {{ leak.secret }} | {{ leak.commit }} | {{ leak.entropy }} | {{ leak.author }} | {{ leak.email }} | {{ leak.date }} | {{ leak.message }} | {{ leak.rule_id }} | {{ leak.fingerprint }} |

{% endfor %}
