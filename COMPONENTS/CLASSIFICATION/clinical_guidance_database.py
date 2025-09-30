#!/usr/bin/env python3
"""
Clinical Guidance Database
Provides actionable clinical guidance for genetic findings
"""

CLINICAL_GUIDANCE = {
    'Long QT syndrome': {
        'genes': ['KCNQ1', 'KCNH2', 'KCNE1', 'KCNE2', 'SCN5A'],
        'condition': 'Long QT Syndrome (LQTS)',
        'severity': 'HIGH - Sudden cardiac death risk',
        'immediate_actions': [
            {
                'action': 'Cardiology Referral',
                'details': 'Refer to electrophysiology within 2 weeks',
                'timeframe': 'URGENT (2 weeks)',
                'icon': '🏥'
            },
            {
                'action': 'Diagnostic Testing',
                'details': 'Baseline ECG with QTc measurement, exercise stress test, Holter monitoring',
                'timeframe': 'IMMEDIATE',
                'icon': '📊'
            },
            {
                'action': 'Medication Review',
                'details': 'Avoid QT-prolonging medications (see crediblemeds.org)',
                'timeframe': 'IMMEDIATE',
                'icon': '💊'
            },
            {
                'action': 'Lifestyle Modifications',
                'details': 'Avoid sudden loud noises (especially for KCNQ1), swimming (KCNQ1), intense exercise',
                'timeframe': 'IMMEDIATE',
                'icon': '⚠️'
            },
            {
                'action': 'Family Screening',
                'details': 'First-degree relatives need ECG screening and genetic testing',
                'timeframe': 'URGENT (within 1 month)',
                'icon': '👨‍👩‍👧‍👦'
            }
        ],
        'monitoring': 'Baseline ECG, repeat ECG if symptoms, annual cardiology follow-up',
        'treatment': 'Beta-blockers (first-line therapy), ICD consideration for high-risk patients, Avoid medication triggers',
        'prognosis': 'With treatment: excellent. Untreated: 13% sudden cardiac death risk by age 40',
        'resources': [
            'Sudden Arrhythmia Death Syndromes Foundation (SADS.org)',
            'Genetic counseling for family planning',
            'crediblemeds.org for QT drug interactions'
        ],
        'next_steps': [
            'Schedule cardiology appointment within 2 weeks',
            'Get ECG at earliest opportunity',
            'Stop any QT-prolonging medications immediately',
            'Contact genetic counselor to discuss family screening',
            'Avoid known triggers based on specific gene'
        ]
    },
    
    'CPVT': {
        'genes': ['RYR2', 'CASQ2'],
        'condition': 'Catecholaminergic Polymorphic Ventricular Tachycardia (CPVT)',
        'severity': 'HIGH - Exercise-induced sudden cardiac death risk',
        'immediate_actions': [
            {
                'action': 'Cardiology Referral',
                'details': 'Urgent referral to electrophysiology',
                'timeframe': 'URGENT (1-2 weeks)',
                'icon': '🏥'
            },
            {
                'action': 'Diagnostic Testing',
                'details': 'Exercise stress test (may unmask arrhythmia), Holter monitoring',
                'timeframe': 'IMMEDIATE',
                'icon': '📊'
            },
            {
                'action': 'Medical Management',
                'details': 'Beta-blocker therapy initiation (nadolol preferred)',
                'timeframe': 'IMMEDIATE',
                'icon': '💊'
            },
            {
                'action': 'Activity Restrictions',
                'details': 'Avoid competitive sports, sudden strenuous exercise, emotional stress',
                'timeframe': 'IMMEDIATE',
                'icon': '⚠️'
            },
            {
                'action': 'Family Cascade Testing',
                'details': 'All first-degree relatives need evaluation',
                'timeframe': 'URGENT (within 1 month)',
                'icon': '👨‍👩‍👧‍👦'
            }
        ],
        'monitoring': 'Exercise stress testing, Holter monitoring, regular cardiology follow-up',
        'treatment': 'Beta-blockers (nadolol preferred), flecainide may be added, ICD for high-risk, left cardiac sympathetic denervation',
        'prognosis': 'First cardiac event often occurs in childhood. 30-50% experience syncope by age 40 if untreated',
        'resources': [
            'CPVT Alliance',
            'Sudden Arrhythmia Death Syndromes Foundation',
            'Genetic counseling'
        ],
        'next_steps': [
            'Urgent cardiology referral (within 1-2 weeks)',
            'Exercise stress test to assess arrhythmia risk',
            'Discuss beta-blocker initiation',
            'Stop all competitive athletics immediately',
            'Family members need cardiac evaluation'
        ]
    },
    
    'Hypertrophic cardiomyopathy': {
        'genes': ['MYH7', 'MYBPC3', 'TNNT2', 'TNNI3', 'TPM1', 'ACTC1', 'MYL2', 'MYL3', 'PRKAG2', 'PLN'],
        'condition': 'Hypertrophic Cardiomyopathy (HCM)',
        'severity': 'MODERATE-HIGH - Progressive condition with SCD risk',
        'immediate_actions': [
            {
                'action': 'Cardiology Referral',
                'details': 'Refer to HCM specialist center',
                'timeframe': 'URGENT (2-4 weeks)',
                'icon': '🏥'
            },
            {
                'action': 'Cardiac Imaging',
                'details': 'Echocardiogram (baseline and serial), consider cardiac MRI',
                'timeframe': 'URGENT (2-4 weeks)',
                'icon': '📊'
            },
            {
                'action': 'Activity Restriction',
                'details': 'Avoid competitive athletics, avoid intense isometric exercise',
                'timeframe': 'IMMEDIATE',
                'icon': '⚠️'
            },
            {
                'action': 'Symptom Management',
                'details': 'Beta-blockers or calcium channel blockers if symptomatic',
                'timeframe': 'AS NEEDED',
                'icon': '💊'
            },
            {
                'action': 'Family Screening',
                'details': 'Echo + ECG for all first-degree relatives, start screening at age 10-12',
                'timeframe': 'URGENT (within 2 months)',
                'icon': '👨‍👩‍👧‍👦'
            }
        ],
        'monitoring': 'Annual echo and ECG, Holter if symptoms, risk stratification for sudden cardiac death',
        'treatment': 'Medications for symptoms (beta-blockers, CCBs), ICD for high SCD risk, septal reduction therapy if obstructive',
        'prognosis': 'Variable - many remain asymptomatic, but sudden cardiac death risk requires assessment',
        'resources': [
            'Hypertrophic Cardiomyopathy Association (HCMA.org)',
            'HCM specialist centers',
            'Genetic counseling'
        ],
        'next_steps': [
            'Schedule cardiology appointment (within 2-4 weeks)',
            'Get baseline echocardiogram and ECG',
            'Stop competitive sports immediately',
            'Discuss with cardiologist about ICD risk assessment',
            'Plan family screening strategy'
        ]
    },
    
    'Dilated cardiomyopathy': {
        'genes': ['TTN', 'LMNA', 'MYH7', 'MYBPC3', 'BAG3', 'FLNC', 'PLN', 'DSP'],
        'condition': 'Dilated Cardiomyopathy (DCM)',
        'severity': 'MODERATE-HIGH - Progressive heart failure risk',
        'immediate_actions': [
            {
                'action': 'Cardiology Referral',
                'details': 'Refer to heart failure specialist',
                'timeframe': 'URGENT (2-4 weeks)',
                'icon': '🏥'
            },
            {
                'action': 'Cardiac Assessment',
                'details': 'Echocardiogram, ECG, BNP/NT-proBNP levels',
                'timeframe': 'URGENT (2 weeks)',
                'icon': '📊'
            },
            {
                'action': 'Medical Therapy',
                'details': 'ACE inhibitor/ARB, beta-blocker, consider aldosterone antagonist',
                'timeframe': 'IMMEDIATE (if symptomatic)',
                'icon': '💊'
            },
            {
                'action': 'Lifestyle Modifications',
                'details': 'Sodium restriction, fluid management, avoid alcohol',
                'timeframe': 'IMMEDIATE',
                'icon': '⚠️'
            },
            {
                'action': 'Family Screening',
                'details': 'Echo + ECG for first-degree relatives every 3-5 years starting at age 10',
                'timeframe': 'URGENT (within 2 months)',
                'icon': '👨‍👩‍👧‍👦'
            }
        ],
        'monitoring': 'Serial echocardiograms, arrhythmia monitoring, assess for heart failure progression',
        'treatment': 'Heart failure medications (ACE-I, beta-blockers, diuretics), ICD/CRT-D consideration, advanced therapies (transplant) if severe',
        'prognosis': 'Variable depending on severity, gene variant, and response to treatment. Regular monitoring essential',
        'resources': [
            'Children\'s Cardiomyopathy Foundation',
            'Heart Failure Society',
            'Genetic counseling'
        ],
        'next_steps': [
            'Schedule cardiology appointment (within 2-4 weeks)',
            'Get baseline echocardiogram and blood work',
            'Discuss heart failure medications if symptomatic',
            'Start lifestyle modifications (low sodium, limit fluids)',
            'Plan family screening'
        ]
    },
    
    'Brugada syndrome': {
        'genes': ['SCN5A', 'SCN1B', 'GPD1L', 'CACNA1C', 'CACNB2'],
        'condition': 'Brugada Syndrome',
        'severity': 'HIGH - Sudden cardiac death risk',
        'immediate_actions': [
            {
                'action': 'Cardiology Referral',
                'details': 'Urgent referral to electrophysiology',
                'timeframe': 'URGENT (1-2 weeks)',
                'icon': '🏥'
            },
            {
                'action': 'Diagnostic Testing',
                'details': 'Baseline ECG, consider sodium channel blocker challenge test',
                'timeframe': 'IMMEDIATE',
                'icon': '📊'
            },
            {
                'action': 'Medication Review',
                'details': 'Avoid sodium channel blocking drugs (see brugadadrugs.org)',
                'timeframe': 'IMMEDIATE',
                'icon': '💊'
            },
            {
                'action': 'Fever Management',
                'details': 'Aggressive fever treatment (increased risk during fever)',
                'timeframe': 'IMMEDIATE',
                'icon': '⚠️'
            },
            {
                'action': 'Family Screening',
                'details': 'ECG screening for all first-degree relatives',
                'timeframe': 'URGENT (within 1 month)',
                'icon': '👨‍👩‍👧‍👦'
            }
        ],
        'monitoring': 'Serial ECGs, consider electrophysiology study, Holter monitoring',
        'treatment': 'ICD for high-risk patients (prior cardiac arrest, syncope), avoid triggers, aggressive fever management',
        'prognosis': 'Highest risk in males age 30-40. Risk stratification essential',
        'resources': [
            'brugadadrugs.org (drug safety)',
            'Sudden Arrhythmia Death Syndromes Foundation',
            'Genetic counseling'
        ],
        'next_steps': [
            'Urgent cardiology referral',
            'Baseline ECG immediately',
            'Review all medications for sodium channel blockers',
            'Plan for aggressive fever treatment',
            'Family screening coordination'
        ]
    }
}

def get_clinical_guidance(condition):
    """Get clinical guidance for a specific condition"""
    return CLINICAL_GUIDANCE.get(condition, None)

def get_guidance_for_gene(gene_symbol):
    """Get clinical guidance based on gene symbol"""
    for condition, guidance in CLINICAL_GUIDANCE.items():
        if gene_symbol in guidance['genes']:
            return guidance
    return None

def format_actionable_summary(condition):
    """Format a human-readable summary of what 'actionable' means for this condition"""
    guidance = get_clinical_guidance(condition)
    
    if not guidance:
        return "Clinical consultation recommended for interpretation."
    
    summary = f"""
CONDITION: {guidance['condition']}
SEVERITY: {guidance['severity']}

WHAT "IMMEDIATELY ACTIONABLE" MEANS FOR YOU:

IMMEDIATE ACTIONS REQUIRED:
"""
    for i, action in enumerate(guidance['immediate_actions'], 1):
        summary += f"\n{i}. {action['icon']} {action['action']} ({action['timeframe']})"
        summary += f"\n   → {action['details']}\n"
    
    summary += f"""
MONITORING NEEDED:
{guidance['monitoring']}

TREATMENT OPTIONS:
{guidance['treatment']}

PROGNOSIS:
{guidance['prognosis']}

YOUR NEXT STEPS (Quick Checklist):
"""
    for i, step in enumerate(guidance['next_steps'], 1):
        summary += f"{i}. {step}\n"
    
    summary += f"""
RESOURCES:
"""
    for resource in guidance['resources']:
        summary += f"• {resource}\n"
    
    return summary

if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("CLINICAL GUIDANCE EXAMPLE: Long QT Syndrome")
    print("=" * 70)
    print(format_actionable_summary('Long QT syndrome'))
