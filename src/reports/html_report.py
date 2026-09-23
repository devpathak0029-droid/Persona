from typing import Dict, Any
import json

def generate_html_report(report_data: Dict[str, Any]) -> str:
    """
    Generate a clean HTML document from the JSON report data using Jinja2.
    """
    try:
        import jinja2
    except ImportError:
        # Fallback if jinja2 is not installed
        return "<html><body><h1>Error: Jinja2 is required to generate HTML reports.</h1></body></html>"
    
    template_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PRALAYX Persona Analysis Report</title>
        <style>
            body { font-family: monospace; background-color: #121212; color: #e0e0e0; margin: 40px; }
            h1, h2, h3 { color: #64b5f6; }
            .section { border: 1px solid #333; padding: 20px; margin-bottom: 20px; border-radius: 5px; }
            table { border-collapse: collapse; width: 100%; margin-top: 10px; }
            th, td { border: 1px solid #444; padding: 8px; text-align: left; }
            th { background-color: #1e1e1e; color: #64b5f6; }
            pre { background-color: #1e1e1e; padding: 10px; overflow-x: auto; border: 1px solid #333; }
        </style>
    </head>
    <body>
        <h1>PRALAYX Persona Analysis Report</h1>
        <p><strong>Version:</strong> {{ report_data.report_version }}</p>
        <p><strong>Generated At:</strong> {{ report_data.generated_at }}</p>
        
        <div class="section">
            <h2>Executive Summary</h2>
            <p>{{ report_data.executive_summary }}</p>
        </div>
        
        <div class="section">
            <h2>Corpus Quality</h2>
            <pre>{{ report_data.corpus_quality | tojson(indent=2) }}</pre>
        </div>
        
        <div class="section">
            <h2>Linguistic Fingerprint</h2>
            <pre>{{ report_data.linguistic_fingerprint | tojson(indent=2) }}</pre>
        </div>
        
        <div class="section">
            <h2>Semantic Profile</h2>
            <pre>{{ report_data.semantic_profile | tojson(indent=2) }}</pre>
        </div>
        
        <div class="section">
            <h2>Behavioral Profile</h2>
            <pre>{{ report_data.behavioral_profile | tojson(indent=2) }}</pre>
        </div>
        
        <div class="section">
            <h2>Persona Evolution</h2>
            <pre>{{ report_data.persona_evolution | tojson(indent=2) }}</pre>
        </div>
        
        <div class="section">
            <h2>Migration Hypotheses</h2>
            <pre>{{ report_data.migration_hypotheses | tojson(indent=2) }}</pre>
        </div>
        
        {% if report_data.cross_persona_comparison %}
        <div class="section">
            <h2>Cross Persona Comparison</h2>
            <pre>{{ report_data.cross_persona_comparison | tojson(indent=2) }}</pre>
        </div>
        {% endif %}
        
        <div class="section">
            <h2>Evidence Ledger</h2>
            {% if report_data.evidence_ledger %}
            <table>
                <tr>
                    <th>Evidence ID</th>
                    <th>Category</th>
                    <th>Feature</th>
                    <th>Confidence</th>
                </tr>
                {% for ev in report_data.evidence_ledger %}
                <tr>
                    <td>{{ ev.evidence_id }}</td>
                    <td>{{ ev.category }}</td>
                    <td>{{ ev.feature }}</td>
                    <td>{{ ev.confidence }}</td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>No evidence recorded.</p>
            {% endif %}
        </div>
        
        {% if report_data.confidence %}
        <div class="section">
            <h2>Confidence & Fusion</h2>
            <pre>{{ report_data.confidence | tojson(indent=2) }}</pre>
        </div>
        {% endif %}
        
        <div class="section">
            <h2>Limitations</h2>
            <ul>
                {% for limit in report_data.limitations %}
                <li>{{ limit }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    
    template = jinja2.Template(template_str)
    
    # Custom filter to dump dicts to json string in jinja
    def tojson_filter(value, indent=None):
        return json.dumps(value, indent=indent)
    
    template.environment.filters['tojson'] = tojson_filter
    
    return template.render(report_data=report_data)
