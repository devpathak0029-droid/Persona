from typing import Dict, Any, Optional

def generate_pdf_report(report_data: Dict[str, Any], output_path: Optional[str] = None) -> Optional[bytes]:
    """
    Generate a basic PDF report using reportlab.
    Returns bytes if successful, None if reportlab is not installed or generation fails.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        from io import BytesIO
    except ImportError:
        return None
        
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        title_style = styles['Title']
        h2_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Title Page
        elements.append(Paragraph("PRALAYX Persona Analysis Report", title_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generated At: {report_data.get('generated_at', 'Unknown')}", normal_style))
        elements.append(Spacer(1, 24))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", h2_style))
        elements.append(Paragraph(str(report_data.get('executive_summary', '')), normal_style))
        elements.append(Spacer(1, 12))
        
        # Corpus Quality
        elements.append(Paragraph("Corpus Quality", h2_style))
        cq = report_data.get('corpus_quality', {})
        cq_text = ", ".join([f"{k}: {v}" for k, v in cq.items()])
        elements.append(Paragraph(cq_text, normal_style))
        elements.append(Spacer(1, 12))
        
        # Evidence Table
        elements.append(Paragraph("Evidence Ledger", h2_style))
        evidence_ledger = report_data.get('evidence_ledger', [])
        
        if evidence_ledger:
            data = [["Evidence ID", "Category", "Feature", "Confidence"]]
            for ev in evidence_ledger:
                data.append([
                    str(ev.get('evidence_id', '')),
                    str(ev.get('category', '')),
                    str(ev.get('feature', '')),
                    str(ev.get('confidence', ''))
                ])
                
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("No evidence recorded.", normal_style))
            
        doc.build(elements)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
                
        return pdf_bytes
        
    except Exception:
        return None
