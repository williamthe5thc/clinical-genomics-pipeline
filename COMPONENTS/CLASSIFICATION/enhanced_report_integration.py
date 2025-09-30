#!/usr/bin/env python3
"""
Enhanced Report Integration
Drop-in addition to your existing pipeline that generates modern HTML reports
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path to import existing modules
sys.path.insert(0, str(Path(__file__).parent))

class EnhancedReportGenerator:
    """Generate modern interactive HTML clinical reports"""
    
    def __init__(self, csv_file, sample_id, output_dir):
        self.csv_file = Path(csv_file)
        self.sample_id = sample_id
        self.output_dir = Path(output_dir)
        self.df = None
        self.stats = {}
        
    def load_data(self):
        """Load and process variant data"""
        print(f"📊 Loading data from {self.csv_file}...")
        self.df = pd.read_csv(self.csv_file)
        print(f"✅ Loaded {len(self.df)} variants")
        self._calculate_statistics()
        
    def _calculate_statistics(self):
        """Calculate comprehensive statistics"""
        self.stats = {
            'total_variants': len(self.df),
            'genes_with_variants': self.df['Gene'].nunique(),
            'immediately_actionable': len(self.df[self.df['Actionability'] == 'IMMEDIATELY_ACTIONABLE']),
            'screening_actionable': len(self.df[self.df['Actionability'] == 'SCREENING_ACTIONABLE']),
            'pathogenic': len(self.df[self.df['ClinVar_Significance'] == 'Pathogenic']),
            'likely_pathogenic': len(self.df[self.df['ClinVar_Significance'] == 'Likely Pathogenic']),
            'vus': len(self.df[self.df['ClinVar_Significance'] == 'Uncertain Significance']),
            'revel_scores': len(self.df[self.df['REVEL_Score'] > 0]),
            'alphamissense_scores': len(self.df[self.df['AlphaMissense_Score'] > 0]),
            'cadd_scores': len(self.df[self.df['CADD_Score'] > 0]),
            'clinvar_annotations': len(self.df[self.df['ClinVar_Significance'] != 'unknown']),
        }
        
        # Specialty breakdown
        self.stats['by_specialty'] = self.df.groupby('Specialty').size().to_dict()
        
    def generate_enhanced_html(self):
        """Generate enhanced interactive HTML report"""
        output_file = self.output_dir / f"{self.sample_id}_enhanced_clinical_report.html"
        
        html = self._generate_html_template()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Enhanced HTML report: {output_file}")
        return output_file
        
    def _generate_html_template(self):
        """Generate complete HTML with embedded data"""
        
        # Prepare top 50 variants for display
        top_variants = self.df.nlargest(min(50, len(self.df)), 'Combined_Score')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Genomics Analysis - {self.sample_id}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{
            animation: fadeIn 0.3s ease-out;
        }}
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
    </style>
</head>
<body class="bg-gradient-to-br from-slate-50 to-blue-50">
    
    <!-- Header -->
    <div class="gradient-bg text-white shadow-xl">
        <div class="max-w-7xl mx-auto px-6 py-8">
            <div class="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <div class="flex items-center gap-3 mb-2">
                        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                        </svg>
                        <h1 class="text-3xl font-bold">Clinical Genomics Analysis</h1>
                    </div>
                    <p class="text-xl opacity-90">Sample: {self.sample_id}</p>
                    <p class="text-sm opacity-75 mt-1">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                <div class="text-right">
                    <div class="text-3xl font-bold">{self.stats['genes_with_variants']}</div>
                    <div class="text-sm opacity-90">Unique Genes</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Important Notice -->
    <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-lg shadow">
            <div class="flex items-start gap-3">
                <svg class="w-6 h-6 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div>
                    <h3 class="font-bold text-amber-900 mb-1">Research Use Only - Clinical Validation Required</h3>
                    <p class="text-sm text-amber-800">
                        This is a <strong>research-grade pipeline</strong> for clinical guidance. All findings require clinical validation before medical decisions. 
                        Consult clinical genetics professionals for interpretation.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- Statistics Cards -->
    <div class="max-w-7xl mx-auto px-6 py-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-red-500 fade-in">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 font-medium">Immediately Actionable</p>
                        <p class="text-3xl font-bold text-red-600 mt-1">{self.stats['immediately_actionable']}</p>
                    </div>
                    <svg class="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-orange-500 fade-in">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 font-medium">Screening Actionable</p>
                        <p class="text-3xl font-bold text-orange-600 mt-1">{self.stats['screening_actionable']}</p>
                    </div>
                    <svg class="w-10 h-10 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-purple-500 fade-in">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 font-medium">Pathogenic Variants</p>
                        <p class="text-3xl font-bold text-purple-600 mt-1">{self.stats['pathogenic']}</p>
                    </div>
                    <svg class="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-blue-500 fade-in">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600 font-medium">Total Variants</p>
                        <p class="text-3xl font-bold text-blue-600 mt-1">{self.stats['total_variants']:,}</p>
                    </div>
                    <svg class="w-10 h-10 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
            </div>
        </div>
    </div>

    <!-- Score Extraction Summary -->
    <div class="max-w-7xl mx-auto px-6 pb-6">
        <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Score Extraction Summary
            </h3>
            <div class="grid md:grid-cols-4 gap-6">
                <div class="text-center p-4 bg-green-50 rounded-lg border border-green-200">
                    <div class="text-3xl font-bold text-green-600 mb-1">{self.stats['revel_scores']}</div>
                    <div class="text-sm text-gray-700">REVEL Scores</div>
                </div>
                <div class="text-center p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div class="text-3xl font-bold text-blue-600 mb-1">{self.stats['alphamissense_scores']}</div>
                    <div class="text-sm text-gray-700">AlphaMissense Scores</div>
                </div>
                <div class="text-center p-4 bg-purple-50 rounded-lg border border-purple-200">
                    <div class="text-3xl font-bold text-purple-600 mb-1">{self.stats['cadd_scores']}</div>
                    <div class="text-sm text-gray-700">CADD Scores</div>
                </div>
                <div class="text-center p-4 bg-orange-50 rounded-lg border border-orange-200">
                    <div class="text-3xl font-bold text-orange-600 mb-1">{self.stats['clinvar_annotations']}</div>
                    <div class="text-sm text-gray-700">ClinVar Annotations</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabs -->
    <div class="max-w-7xl mx-auto px-6">
        <div class="bg-white rounded-t-lg shadow-md">
            <div class="flex border-b border-gray-200">
                <button onclick="showTab('overview')" id="tab-overview" class="tab-button px-6 py-3 font-medium border-b-2 border-indigo-600 text-indigo-600">
                    Clinical Overview
                </button>
                <button onclick="showTab('variants')" id="tab-variants" class="tab-button px-6 py-3 font-medium text-gray-600 hover:text-gray-900">
                    Top Variants ({min(50, len(self.df))})
                </button>
                <button onclick="showTab('specialties')" id="tab-specialties" class="tab-button px-6 py-3 font-medium text-gray-600 hover:text-gray-900">
                    By Specialty
                </button>
            </div>
        </div>
    </div>

    <!-- Tab Content -->
    <div class="max-w-7xl mx-auto px-6 pb-8">
        <div class="bg-white rounded-b-lg shadow-md p-6">
            
            <!-- Overview Tab -->
            <div id="content-overview" class="tab-content">
                <div class="grid md:grid-cols-3 gap-6 mb-6">
                    {self._generate_specialty_cards()}
                </div>
                
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 class="font-bold text-blue-900 mb-4 flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Analysis Summary
                    </h3>
                    <div class="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                            <p class="font-semibold text-gray-700 mb-2">Coverage:</p>
                            <ul class="space-y-1 text-gray-600">
                                <li>• 22 medical specialties analyzed</li>
                                <li>• 790 clinically relevant genes</li>
                                <li>• ACMG Secondary Findings v3.3 included</li>
                                <li>• Comprehensive pathogenicity predictions</li>
                            </ul>
                        </div>
                        <div>
                            <p class="font-semibold text-gray-700 mb-2">Data Sources:</p>
                            <ul class="space-y-1 text-gray-600">
                                <li>• gnomAD v4.1 population frequencies</li>
                                <li>• ClinVar September 2025 release</li>
                                <li>• REVEL, AlphaMissense, CADD scores</li>
                                <li>• VEP v114.2 comprehensive annotation</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Variants Tab -->
            <div id="content-variants" class="tab-content hidden">
                <div class="space-y-3" id="variants-container">
                    {self._generate_variant_cards(top_variants)}
                </div>
            </div>

            <!-- Specialties Tab -->
            <div id="content-specialties" class="tab-content hidden">
                <div class="space-y-4">
                    {self._generate_specialty_sections()}
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="max-w-7xl mx-auto px-6 pb-8">
        <div class="bg-white rounded-lg shadow-md p-6 text-center text-sm text-gray-600">
            <p class="mb-2">
                <strong>Clinical Genomics Pipeline v4.0</strong> | 
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
            <p>
                This report is for <strong>research use only</strong> and requires clinical validation. 
                Consult with clinical genetics professionals for interpretation and medical decision-making.
            </p>
        </div>
    </div>

    <script>
        function showTab(tabName) {{
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.add('hidden'));
            
            // Remove active class from all tabs
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(button => {{
                button.classList.remove('border-b-2', 'border-indigo-600', 'text-indigo-600');
                button.classList.add('text-gray-600');
            }});
            
            // Show selected tab
            document.getElementById('content-' + tabName).classList.remove('hidden');
            
            // Add active class to selected tab
            const activeButton = document.getElementById('tab-' + tabName);
            activeButton.classList.add('border-b-2', 'border-indigo-600', 'text-indigo-600');
            activeButton.classList.remove('text-gray-600');
        }}

        function toggleVariant(index) {{
            const details = document.getElementById('variant-details-' + index);
            const icon = document.getElementById('variant-icon-' + index);
            
            if (details.classList.contains('hidden')) {{
                details.classList.remove('hidden');
                icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />`;
            }} else {{
                details.classList.add('hidden');
                icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />`;
            }}
        }}
    </script>
</body>
</html>"""
        return html
    
    def _generate_specialty_cards(self):
        """Generate specialty summary cards"""
        specialty_config = {
            'CARDIAC': ('Cardiac Findings', 'from-red-50 to-pink-50', 'red'),
            'ONCOLOGY': ('Oncology Findings', 'from-purple-50 to-indigo-50', 'purple'),
            'CDLS': ('CdLS Findings', 'from-blue-50 to-cyan-50', 'blue')
        }
        
        cards_html = ""
        for specialty, (title, gradient, color) in specialty_config.items():
            count = self.stats['by_specialty'].get(specialty, 0)
            cards_html += f"""
                <div class="bg-gradient-to-br {gradient} p-6 rounded-lg border border-{color}-200">
                    <h3 class="font-bold text-{color}-900 mb-3 flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        {title}
                    </h3>
                    <div class="text-3xl font-bold text-{color}-600 mb-2">{count}</div>
                    <p class="text-sm text-{color}-700">Variants in {specialty.lower()} genes</p>
                </div>
            """
        return cards_html
    
    def _generate_variant_cards(self, variants_df):
        """Generate variant detail cards"""
        cards_html = ""
        for idx, (_, variant) in enumerate(variants_df.iterrows()):
            actionability_colors = {
                'IMMEDIATELY_ACTIONABLE': ('bg-red-100', 'text-red-800', 'border-red-300'),
                'SCREENING_ACTIONABLE': ('bg-orange-100', 'text-orange-800', 'border-orange-300'),
                'FAMILY_ACTIONABLE': ('bg-yellow-100', 'text-yellow-800', 'border-yellow-300'),
                'COUNSELING_INDICATED': ('bg-blue-100', 'text-blue-800', 'border-blue-300'),
            }
            
            bg, text, border = actionability_colors.get(variant['Actionability'], ('bg-gray-100', 'text-gray-800', 'border-gray-300'))
            
            clinvar_color = self._get_clinvar_color(variant['ClinVar_Significance'])
            revel_color = self._get_score_color(variant.get('REVEL_Score', 0), 'REVEL')
            cadd_color = self._get_score_color(variant.get('CADD_Score', 0), 'CADD')
            
            # Safe formatting for all values
            gene = str(variant.get('Gene', 'Unknown'))
            chromosome = str(variant.get('Chromosome', '?'))
            position = str(variant.get('Position', '?'))
            ref = str(variant.get('Ref', '?'))
            alt = str(variant.get('Alt', '?'))
            consequence = str(variant.get('Consequence', 'unknown'))
            condition = str(variant.get('Condition', 'Unknown condition'))
            
            cards_html += f"""
                <div class="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                    <div class="p-4 cursor-pointer hover:bg-gray-50" onclick="toggleVariant({idx})">
                        <div class="flex items-start justify-between gap-4">
                            <div class="flex-1 min-w-0">
                                <div class="flex items-center gap-3 mb-2 flex-wrap">
                                    <span class="text-lg font-bold text-indigo-600">{gene}</span>
                                    <span class="px-3 py-1 rounded-full text-xs font-medium border {bg} {text} {border}">
                                        {variant['Actionability'].replace('_', ' ')}
                                    </span>
                                    <span class="text-sm font-medium {clinvar_color}">
                                        {variant['ClinVar_Significance']}
                                    </span>
                                </div>
                                <p class="text-sm text-gray-700 mb-1">{condition}</p>
                                <p class="text-xs text-gray-500">
                                    chr{chromosome}:{position} {ref}→{alt} | {consequence}
                                </p>
                            </div>
                            
                            <div class="flex items-center gap-6 flex-shrink-0">
                                <div class="text-right">
                                    <div class="text-xs text-gray-500 mb-1">REVEL</div>
                                    <div class="text-lg font-bold {revel_color}">
                                        {variant.get('REVEL_Score', 0):.3f}
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div class="text-xs text-gray-500 mb-1">CADD</div>
                                    <div class="text-lg font-bold {cadd_color}">
                                        {variant.get('CADD_Score', 0):.1f}
                                    </div>
                                </div>
                                <div class="text-right">
                                    <div class="text-xs text-gray-500 mb-1">Score</div>
                                    <div class="text-lg font-bold text-purple-600">
                                        {int(variant['Combined_Score'])}
                                    </div>
                                </div>
                                <svg id="variant-icon-{idx}" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <div id="variant-details-{idx}" class="hidden border-t border-gray-200 bg-gray-50 p-4">
                        <div class="grid md:grid-cols-3 gap-6 text-sm">
                            <div>
                                <h4 class="font-semibold text-gray-700 mb-3">Clinical Information</h4>
                                <dl class="space-y-2">
                                    <div>
                                        <dt class="text-gray-600 font-medium">Evidence Tier:</dt>
                                        <dd class="text-gray-900">{variant['Evidence_Tier'].replace('_', ' ')}</dd>
                                    </div>
                                    <div>
                                        <dt class="text-gray-600 font-medium">Source:</dt>
                                        <dd class="text-gray-900">{variant['Source']}</dd>
                                    </div>
                                    <div>
                                        <dt class="text-gray-600 font-medium">Specialty:</dt>
                                        <dd class="text-gray-900">{variant['Specialty']}</dd>
                                    </div>
                                </dl>
                            </div>
                            
                            <div>
                                <h4 class="font-semibold text-gray-700 mb-3">Pathogenicity Scores</h4>
                                <dl class="space-y-2">
                                    <div class="flex justify-between">
                                        <dt class="text-gray-600 font-medium">REVEL:</dt>
                                        <dd class="font-semibold {revel_color}">
                                            {variant.get('REVEL_Score', 0):.3f if variant.get('REVEL_Score', 0) > 0 else 'N/A'}
                                        </dd>
                                    </div>
                                    <div class="flex justify-between">
                                        <dt class="text-gray-600 font-medium">AlphaMissense:</dt>
                                        <dd class="font-semibold {self._get_score_color(variant.get('AlphaMissense_Score', 0), 'AlphaMissense')}">
                                            {variant.get('AlphaMissense_Score', 0):.3f if variant.get('AlphaMissense_Score', 0) > 0 else 'N/A'}
                                        </dd>
                                    </div>
                                    <div class="flex justify-between">
                                        <dt class="text-gray-600 font-medium">CADD:</dt>
                                        <dd class="font-semibold {cadd_color}">
                                            {variant.get('CADD_Score', 0):.1f if variant.get('CADD_Score', 0) > 0 else 'N/A'}
                                        </dd>
                                    </div>
                                </dl>
                            </div>
                            
                            <div>
                                <h4 class="font-semibold text-gray-700 mb-3">Population Data</h4>
                                <dl class="space-y-2">
                                    <div>
                                        <dt class="text-gray-600 font-medium">gnomAD AF:</dt>
                                        <dd class="text-gray-900 font-mono text-xs">
                                            {self._format_frequency(variant.get('gnomAD_AF', 1.0))}
                                        </dd>
                                    </div>
                                    <div>
                                        <dt class="text-gray-600 font-medium">Variant Score:</dt>
                                        <dd class="text-gray-900">{int(variant['Variant_Score'])}</dd>
                                    </div>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            """
        return cards_html
    
    def _generate_specialty_sections(self):
        """Generate specialty-specific sections"""
        sections_html = ""
        for specialty in sorted(self.stats['by_specialty'].keys()):
            if pd.isna(specialty):
                continue
                
            specialty_df = self.df[self.df['Specialty'] == specialty].nlargest(10, 'Combined_Score')
            
            sections_html += f"""
                <div class="border border-gray-200 rounded-lg p-6">
                    <h3 class="text-xl font-bold text-gray-900 mb-4">{specialty}</h3>
                    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
            """
            
            for _, v in specialty_df.iterrows():
                clinvar_color = self._get_clinvar_color(v['ClinVar_Significance'])
                gene = str(v.get('Gene', 'Unknown'))
                condition = str(v.get('Condition', 'Unknown condition'))
                sections_html += f"""
                    <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                        <div class="font-bold text-indigo-600 mb-1">{gene}</div>
                        <div class="text-sm text-gray-700 mb-2 truncate" title="{condition}">{condition}</div>
                        <div class="flex justify-between text-xs">
                            <span class="{clinvar_color}">
                                {v['ClinVar_Significance']}
                            </span>
                            <span class="font-semibold text-purple-600">
                                Score: {int(v['Combined_Score'])}
                            </span>
                        </div>
                    </div>
                """
            
            sections_html += """
                    </div>
                </div>
            """
        return sections_html
    
    def _get_clinvar_color(self, sig):
        """Get color class for ClinVar significance"""
        sig_str = str(sig)
        if sig_str == 'Pathogenic':
            return 'text-red-600 font-bold'
        elif sig_str == 'Likely Pathogenic':
            return 'text-orange-600 font-semibold'
        elif sig_str == 'Uncertain Significance':
            return 'text-gray-600'
        elif 'Benign' in sig_str:
            return 'text-green-600'
        return 'text-gray-400'
    
    def _get_score_color(self, score, score_type):
        """Get color class for pathogenicity scores"""
        if score_type in ['REVEL', 'AlphaMissense']:
            if score >= 0.75:
                return 'text-red-600 font-bold'
            elif score >= 0.5:
                return 'text-orange-600 font-semibold'
            elif score >= 0.3:
                return 'text-yellow-600'
            return 'text-gray-500'
        elif score_type == 'CADD':
            if score >= 25:
                return 'text-red-600 font-bold'
            elif score >= 15:
                return 'text-orange-600'
            return 'text-gray-500'
        return 'text-gray-600'
    
    def _format_frequency(self, freq):
        """Format allele frequency for display"""
        try:
            freq_val = float(freq)
            if freq_val == 0 or freq_val >= 1.0:
                return 'Not found'
            elif freq_val < 0.00001:
                return '<0.00001'
            else:
                return f'{freq_val:.2e}'
        except:
            return 'Not found'

def integrate_enhanced_report(csv_file, sample_id, output_dir):
    """
    Call this function from your main pipeline to add enhanced HTML reports
    
    Usage:
        from enhanced_report_integration import integrate_enhanced_report
        integrate_enhanced_report(csv_file, sample_id, output_dir)
    """
    print("\n" + "="*70)
    print("🎨 Generating Enhanced Clinical Report...")
    print("="*70)
    
    try:
        generator = EnhancedReportGenerator(csv_file, sample_id, output_dir)
        generator.load_data()
        html_file = generator.generate_enhanced_html()
        
        print(f"\n✅ Enhanced report ready: {html_file}")
        print("📱 Mobile-friendly, interactive design")
        print("🎯 Professional clinical presentation")
        print("="*70 + "\n")
        
        return html_file
        
    except Exception as e:
        print(f"\n❌ Error generating enhanced report: {e}")
        print("   Continuing with standard reports...")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python enhanced_report_integration.py <csv_file> <sample_id> <output_dir>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    sample_id = sys.argv[2]
    output_dir = sys.argv[3]
    
    integrate_enhanced_report(csv_file, sample_id, output_dir)
