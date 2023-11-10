## Structure Report

### Git Information
Is Git Repository: {{ data.is_git_repository }}
{% if data.git_repository_hash %}
Commit Hash: {{ data.git_repository_hash }}
{% endif %}

### Project Structure
{% macro render_directory(item, prefix='') -%}
{{ prefix }}- {{ item.name }}
  {%- if item.type == "directory" and item.contents %}
    {%- for subitem in item.contents %}
      {{ render_directory(subitem, prefix + '    ') }}
    {%- endfor %}
  {%- endif %}
{%- endmacro %}

```
{% for item in data.structure %}
{{ render_directory(item) }}
{% endfor %}
```

### Configuration Files
Has Precommit File: {{ data.has_precommit_file }}
{% if data.has_precommit_file %}
#### Pre-commit hooks
{% for repo in data.precommit_config.repos %}
- {{ repo.repo }}
  {%- for hook in repo.hooks %}
    - {{ hook.id }} : {{ hook.name | default(hook.id) }}
  {%- endfor %}
{% endfor %}
{% endif %}

### Testing
Has Tests: {{ data.has_tests }}  
Uses Pytest: {{ data.uses_pytest }}  
{% if data.uses_pytest and data.coverage %}
Coverage: {{ data.coverage['totals']['percent_covered_display'] }}%
{% endif %}

### Dependencies Detection
{% for dep, exists in data.dependencies.items() %}
- {{ dep }}: {{ exists }}
{% endfor %}
