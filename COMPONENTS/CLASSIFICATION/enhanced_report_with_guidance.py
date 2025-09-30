#!/usr/bin/env python3
"""
Enhanced Report Generator with Clinical Guidance
Now includes ACTUAL actionable clinical guidance, not just labels!
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Import clinical guidance database
try:
    from clinical_guidance_database import get_clinical_guidance, format_actionable_summary
    GUIDANCE_AVAILABLE = True
except ImportError:
    GUIDANCE_AVAILABLE = False
    print("⚠️  Clinical guidance database not found. Reports will include basic information only.")

class EnhancedReportWithGuidance:
    """Generate reports with actual clinical guidance"""
    
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
            'revel_scores': len(self.df[self.df['REVEL_Score'] > 0]),
            'alphamissense_scores': len(self.df[self.df['AlphaMissense_Score'] > 0]),
            'cadd_scores': len(self.df[self.df['CADD_Score'] > 0]),
            'clinvar_annotations': len(self.df[self.df['ClinVar_Significance'] != 'unknown']),
        }
        self.stats['by_specialty'] = self.df.groupby('Specialty').size().to_dict()
        
    def generate_enhanced_html_with_guidance(self):
        """Generate enhanced HTML report with clinical guidance"""
        output_file = self.output_dir / f"{self.sample_id}_enhanced_clinical_report_with_guidance.html"
        
        html = self._generate_html_with_guidance()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Enhanced HTML report with clinical guidance: {output_file}")
        return output_file
    
    def _generate_html_with_guidance(self):
        """Generate complete HTML with clinical guidance"""
        
        # Get immediately actionable variants
        actionable_variants = self.df[self.df['Actionability'] == 'IMMEDIATELY_ACTIONABLE'].nlargest(20, 'Combined_Score')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Genomics Report with Actionable Guidance - {self.sample_id}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-header {{ background: linear-gradient(135deg, #dc2626 0%, #e11d48 50%, #9333ea 100%); }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
        .pulse-animation {{ animation: pulse 2s ease-in-out infinite; }}
    </style>
</head>
<body class="bg-gradient-to-br from-slate-50 to-blue-50">

    <!-- URGENT Header -->
    <div class="gradient-header text-white shadow-2xl">
        <div class="max-w-7xl mx-auto px-6 py-8">
            <div class="flex items-center gap-4 mb-4">
                <svg class="w-12 h-12 pulse-animation" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div>
                    <h1 class="text-4xl font-bold">Clinical Action Required</h1>
                    <p class="text-xl opacity-90 mt-1">Immediate clinical follow-up needed</p>
                </div>
            </div>
            <div class="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                <p class="text-lg">
                    <strong>Sample:</strong> {self.sample_id} | 
                    <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')} |
                    <strong>Actionable Findings:</strong> {self.stats['immediately_actionable']}
                </p>
            </div>
        </div>
    </div>

    <!-- What "Actionable" Means Section -->
    <div class="max-w-7xl mx-auto px-6 py-6">
        <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h2 class="text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                What Does "Immediately Actionable" Actually Mean?
            </h2>
            
            <div class="bg-red-50 border-l-4 border-red-600 p-6 rounded-r-lg mb-6">
                <h3 class="font-bold text-red-900 text-xl mb-3">Plain English Definition</h3>
                <p class="text-red-800 mb-4 text-lg">
                    <strong>"Immediately Actionable"</strong> means you need to schedule medical appointments 
                    and tests within the next 1-4 weeks. It does NOT mean you have an emergency right now.
                </p>
                <p class="text-red-800 text-lg">
                    These genetic variants are associated with conditions that:
                </p>
                <ul class="list-disc list-inside text-red-800 mt-3 space-y-2 text-lg ml-4">
                    <li>Can cause serious problems <em>if left unmanaged</em></li>
                    <li>Have proven medical treatments that work</li>
                    <li>Benefit from early detection and monitoring</li>
                    <li>May affect your family members (they should be tested too)</li>
                </ul>
            </div>

            <div class="grid md:grid-cols-2 gap-6 mb-6">
                <div class="bg-orange-50 border-2 border-orange-400 rounded-lg p-6">
                    <h4 class="font-bold text-orange-900 text-xl mb-3">❌ This Does NOT Mean:</h4>
                    <ul class="text-orange-800 space-y-2 text-base">
                        <li>• You have a medical emergency</li>
                        <li>• You definitely have symptoms now</li>
                        <li>• The condition will definitely develop</li>
                        <li>• You need to go to the ER</li>
                        <li>• Treatment must start today</li>
                    </ul>
                </div>

                <div class="bg-green-50 border-2 border-green-400 rounded-lg p-6">
                    <h4 class="font-bold text-green-900 text-xl mb-3">✅ This DOES Mean:</h4>
                    <ul class="text-green-800 space-y-2 text-base">
                        <li>• Schedule specialist appointments (1-4 weeks)</li>
                        <li>• Get confirmatory testing done</li>
                        <li>• Start recommended monitoring</li>
                        <li>• Inform your family members</li>
                        <li>• Meet with a genetic counselor</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Statistics Dashboard -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                <div class="text-3xl font-bold text-red-600 mb-2">{self.stats['immediately_actionable']}</div>
                <div class="text-sm text-gray-700">Immediately Actionable</div>
            </div>
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
                <div class="text-3xl font-bold text-orange-600 mb-2">{self.stats['screening_actionable']}</div>
                <div class="text-sm text-gray-700">Screening Actionable</div>
            </div>
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
                <div class="text-3xl font-bold text-purple-600 mb-2">{self.stats['pathogenic']}</div>
                <div class="text-sm text-gray-700">Pathogenic Variants</div>
            </div>
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                <div class="text-3xl font-bold text-blue-600 mb-2">{self.stats['total_variants']:,}</div>
                <div class="text-sm text-gray-700">Total Variants</div>
            </div>
        </div>

        <!-- Actionable Variants with Clinical Guidance -->
        <div class="space-y-6">
            {self._generate_actionable_variants_with_guidance(actionable_variants)}
        </div>

        <!-- Important Disclaimer -->
        <div class="bg-amber-50 border-l-4 border-amber-600 rounded-r-lg p-6 mt-6">
            <h3 class="font-bold text-amber-900 text-xl mb-3 flex items-center gap-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                CRITICAL: Research Use Only
            </h3>
            <ul class="text-amber-800 space-y-2 text-base">
                <li>• <strong>This is research-grade analysis</strong> - requires clinical confirmation</li>
                <li>• <strong>All findings must be confirmed</strong> by CLIA-certified laboratory</li>
                <li>• <strong>Consult medical genetics professionals</strong> for interpretation</li>
                <li>• <strong>Do not make medical decisions</strong> based solely on this report</li>
                <li>• <strong>Clinical correlation required</strong> with personal and family history</li>
            </ul>
        </div>
    </div>

    <script>
        function toggleGuidance(index) {{
            const element = document.getElementById('guidance-' + index);
            const icon = document.getElementById('icon-' + index);
            if (element.classList.contains('hidden')) {{
                element.classList.remove('hidden');
                icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />`;
            }} else {{
                element.classList.add('hidden');
                icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />`;
            }}
        }}
    </script>
</body>
</html>"""
        return html
    
    def _generate_actionable_variants_with_guidance(self, variants_df):
        """Generate variant cards with clinical guidance"""
        cards_html = ""
        
        for idx, (_, variant) in enumerate(variants_df.iterrows()):
            condition = variant.get('Condition', 'Unknown')
            gene = variant.get('Gene', 'Unknown')
            
            # Get clinical guidance if available
            guidance = None
            if GUIDANCE_AVAILABLE:
                guidance = get_clinical_guidance(condition)
            
            cards_html += f"""
                <div class="bg-white rounded-lg shadow-lg overflow-hidden border-2 border-red-200">
                    <!-- Variant Header -->
                    <div class="bg-gradient-to-r from-red-50 to-pink-50 p-6 cursor-pointer hover:bg-red-100 transition-colors" onclick="toggleGuidance({idx})">
                        <div class="flex items-start justify-between gap-4">
                            <div class="flex-1">
                                <div class="flex items-center gap-3 mb-3">
                                    <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                    </svg>
                                    <h3 class="text-2xl font-bold text-gray-900">{gene}</h3>
                                    <span class="px-4 py-1 bg-red-500 text-white rounded-full text-sm font-bold">
                                        ACTIONABLE
                                    </span>
                                    {f'<span class="px-4 py-1 bg-purple-500 text-white rounded-full text-sm font-bold">{variant["ClinVar_Significance"]}</span>' if variant.get('ClinVar_Significance') == 'Pathogenic' else ''}
                                </div>
                                <p class="text-xl text-gray-800 font-semibold mb-2">{condition}</p>
                                <p class="text-sm text-gray-600">chr{variant.get('Chromosome', '?')}:{variant.get('Position', '?')} {variant.get('Ref', '?')}→{variant.get('Alt', '?')}</p>
                            </div>
                            <div class="flex items-center gap-4">
                                <div class="text-right">
                                    <div class="text-xs text-gray-500 mb-1">REVEL</div>
                                    <div class="text-lg font-bold text-gray-900">{variant.get('REVEL_Score', 0):.3f}</div>
                                </div>
                                <div class="text-right">
                                    <div class="text-xs text-gray-500 mb-1">CADD</div>
                                    <div class="text-lg font-bold text-gray-900">{variant.get('CADD_Score', 0):.1f}</div>
                                </div>
                                <svg id="icon-{idx}" class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Clinical Guidance - Expandable -->
                    <div id="guidance-{idx}" class="hidden border-t-2 border-red-200">
                        {self._format_guidance_section(guidance, condition) if guidance else self._format_no_guidance_section(condition)}
                    </div>
                </div>
            """
        
        return cards_html
    
    def _format_guidance_section(self, guidance, condition):
        """Format the clinical guidance section"""
        html = f"""
            <div class="p-6 bg-gray-50">
                <!-- Severity Alert -->
                <div class="bg-red-100 border-2 border-red-500 rounded-lg p-4 mb-6">
                    <h4 class="font-bold text-red-900 text-xl mb-2">{guidance['condition']}</h4>
                    <p class="text-red-800 text-lg font-semibold">{guidance['severity']}</p>
                </div>
                
                <!-- Immediate Actions Required -->
                <div class="mb-6">
                    <h4 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Immediate Actions You Need to Take
                    </h4>
                    <div class="space-y-3">
        """
        
        for action in guidance['immediate_actions']:
            priority_colors = {
                'URGENT': 'border-red-500 bg-red-50',
                'IMMEDIATE': 'border-orange-500 bg-orange-50',
                'AS NEEDED': 'border-blue-500 bg-blue-50'
            }
            
            timeframe = action['timeframe']
            priority_class = 'URGENT' if 'URGENT' in timeframe else 'IMMEDIATE' if 'IMMEDIATE' in timeframe else 'AS NEEDED'
            color_class = priority_colors.get(priority_class, 'border-gray-500 bg-gray-50')
            
            html += f"""
                <div class="border-l-4 {color_class} p-4 rounded-r-lg">
                    <div class="flex items-start gap-3">
                        <div class="text-2xl">{action['icon']}</div>
                        <div class="flex-1">
                            <h5 class="font-bold text-gray-900 mb-1 text-lg">{action['action']}</h5>
                            <p class="text-gray-700 mb-2">{action['details']}</p>
                            <span class="inline-block px-3 py-1 bg-gray-900 text-white rounded-full text-xs font-bold">
                                {timeframe}
                            </span>
                        </div>
                    </div>
                </div>
            """
        
        html += f"""
                    </div>
                </div>
                
                <!-- Clinical Details Grid -->
                <div class="grid md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white rounded-lg border-2 border-blue-200 p-5">
                        <h5 class="font-bold text-blue-900 text-lg mb-3">📋 Required Monitoring</h5>
                        <p class="text-gray-700">{guidance['monitoring']}</p>
                    </div>
                    
                    <div class="bg-white rounded-lg border-2 border-green-200 p-5">
                        <h5 class="font-bold text-green-900 text-lg mb-3">💊 Treatment Options</h5>
                        <p class="text-gray-700">{guidance['treatment']}</p>
                    </div>
                    
                    <div class="bg-white rounded-lg border-2 border-purple-200 p-5">
                        <h5 class="font-bold text-purple-900 text-lg mb-3">📊 What to Expect</h5>
                        <p class="text-gray-700">{guidance['prognosis']}</p>
                    </div>
                    
                    <div class="bg-white rounded-lg border-2 border-orange-200 p-5">
                        <h5 class="font-bold text-orange-900 text-lg mb-3">🔗 Helpful Resources</h5>
                        <ul class="text-gray-700 space-y-1">
        """
        
        for resource in guidance['resources']:
            html += f"                    <li>• {resource}</li>\n"
        
        html += """
                        </ul>
                    </div>
                </div>
                
                <!-- Next Steps Checklist -->
                <div class="bg-blue-50 border-2 border-blue-400 rounded-lg p-6">
                    <h5 class="font-bold text-blue-900 text-xl mb-4">🎯 Your Next Steps (Checklist)</h5>
                    <ol class="space-y-2 text-blue-900">
        """
        
        for i, step in enumerate(guidance['next_steps'], 1):
            html += f"                    <li class='text-base'><strong>{i}.</strong> {step}</li>\n"
        
        html += """
                    </ol>
                </div>
            </div>
        """
        
        return html
    
    def _format_no_guidance_section(self, condition):
        """Format section when specific guidance not available"""
        return f"""
            <div class="p-6 bg-gray-50">
                <div class="bg-blue-50 border-2 border-blue-400 rounded-lg p-6">
                    <h4 class="font-bold text-blue-900 text-xl mb-3">Clinical Consultation Recommended</h4>
                    <p class="text-blue-800 mb-4">
                        Specific guidance for <strong>{condition}</strong> is not available in this automated report, 
                        but this finding is flagged as clinically actionable.
                    </p>
                    <h5 class="font-bold text-blue-900 mb-2">Recommended Actions:</h5>
                    <ol class="text-blue-800 space-y-2">
                        <li>1. Schedule appointment with medical genetics or genetic counselor</li>
                        <li>2. Get confirmatory testing at CLIA-certified laboratory</li>
                        <li>3. Discuss with appropriate medical specialist for this condition</li>
                        <li>4. Consider family screening after confirmation</li>
                        <li>5. Document findings in medical record</li>
                    </ol>
                </div>
            </div>
        """

def main():
    if len(sys.argv) < 4:
        print("Usage: python enhanced_report_with_guidance.py <csv_file> <sample_id> <output_dir>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    sample_id = sys.argv[2]
    output_dir = sys.argv[3]
    
    print("\n" + "=" * 70)
    print("🎯 Enhanced Clinical Report with ACTIONABLE GUIDANCE")
    print("=" * 70)
    print()
    
    generator = EnhancedReportWithGuidance(csv_file, sample_id, output_dir)
    generator.load_data()
    html_file = generator.generate_enhanced_html_with_guidance()
    
    print("\n✅ Report with clinical guidance complete!")
    print(f"📄 Open this file to see REAL actionable guidance: {html_file}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
