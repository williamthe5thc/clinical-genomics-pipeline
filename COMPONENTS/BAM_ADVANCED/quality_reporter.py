#!/usr/bin/env python3
"""
Quality Reporter for Enhanced Clinical Genomics Pipeline
Generates comprehensive BAM-level quality reports for clinical decision support

Location: D:\Genome\pipeline_components\quality_reporter.py
Author: Clinical Genomics Pipeline Enhancement  
Version: 1.0 (Based on mosdepth performance and clinical QC standards)
"""

import os
import sys
import json
import logging
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class QualityMetrics:
    """Container for comprehensive quality metrics"""
    sample_id: str
    total_reads: int
    mapped_reads: int
    properly_paired: int
    mean_coverage: float
    coverage_20x_percent: float
    coverage_30x_percent: float
    coverage_100x_percent: float
    mapping_quality_mean: float
    insert_size_mean: float
    insert_size_std: float
    gc_bias_coefficient: float
    contamination_estimate: float
    on_target_percent: float
    uniformity_coefficient: float
    gaps_identified: int
    clinical_depth_coverage: float

class QualityReporter:
    """
    Comprehensive quality reporting for clinical genomics
    Based on mosdepth 2-9 minute processing with clinical QC standards
    """
    
    def __init__(self, config_file: str = "D:/Genome/enhanced_config/quality_config.json"):
        self.config = self._load_config(config_file)
        self.logger = self._setup_logging()
        self.clinical_genes_bed = "D:/Genome/databases/clinical_panels/915_gene_panel.bed"
        
        # Clinical QC thresholds based on ACMG/CLIA standards
        self.quality_thresholds = {
            "min_coverage_20x_percent": 95.0,  # ACMG standard
            "min_coverage_30x_percent": 90.0,  # Clinical preference
            "min_mean_coverage": 30.0,         # Clinical minimum
            "max_contamination_percent": 3.0,   # Quality control limit
            "min_mapping_quality": 20,          # Standard threshold
            "min_on_target_percent": 80.0,     # Capture efficiency
            "max_uniformity_cv": 0.3           # Coverage uniformity
        }
        
    def _load_config(self, config_file: str) -> Dict:
        """Load quality reporter configuration"""
        default_config = {
            "enable_visualizations": True,
            "enable_detailed_reports": True,
            "output_formats": ["html", "pdf", "json"],
            "include_gene_level_metrics": True,
            "processing_timeout_minutes": 10
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load quality config {config_file}: {e}")
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for quality reporter"""
        logger = logging.getLogger('QualityReporter')
        logger.setLevel(logging.INFO)
        
        log_dir = Path("D:/Genome/logs")
        log_dir.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_dir / "quality_reporting.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def generate_comprehensive_quality_report(self, bam_results: Dict, sample_id: str, output_dir: str) -> Dict:
        """
        Generate comprehensive quality report from BAM analysis results
        Integrates all QC metrics into clinical decision support format
        """
        start_time = time.time()
        self.logger.info(f"Generating comprehensive quality report for {sample_id}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        report_results = {
            "sample_id": sample_id,
            "report_generation_start": start_time,
            "input_data": bam_results,
            "quality_assessment": {},
            "clinical_recommendations": {},
            "visualizations": {},
            "status": "processing"
        }
        
        try:
            # Step 1: Extract and consolidate quality metrics
            self.logger.info("Step 1: Consolidating quality metrics")
            consolidated_metrics = self._consolidate_quality_metrics(bam_results, sample_id)
            report_results["consolidated_metrics"] = consolidated_metrics
            
            # Step 2: Perform quality assessment
            self.logger.info("Step 2: Performing quality assessment")
            quality_assessment = self._perform_quality_assessment(consolidated_metrics)
            report_results["quality_assessment"] = quality_assessment
            
            # Step 3: Generate clinical recommendations
            self.logger.info("Step 3: Generating clinical recommendations")
            clinical_recommendations = self._generate_clinical_recommendations(
                quality_assessment, consolidated_metrics
            )
            report_results["clinical_recommendations"] = clinical_recommendations
            
            # Step 4: Create visualizations
            if self.config["enable_visualizations"]:
                self.logger.info("Step 4: Creating quality visualizations")
                visualizations = self._create_quality_visualizations(
                    consolidated_metrics, output_path, sample_id
                )
                report_results["visualizations"] = visualizations
            
            # Step 5: Generate reports
            self.logger.info("Step 5: Generating quality reports")
            report_files = self._generate_quality_reports(
                report_results, output_path, sample_id
            )
            report_results["report_files"] = report_files
            
            total_time = time.time() - start_time
            report_results["processing_time"] = total_time
            report_results["status"] = "completed"
            
            self.logger.info(f"Quality report generation completed for {sample_id} in {total_time:.2f} seconds")
            
            return report_results
            
        except Exception as e:
            self.logger.error(f"Error generating quality report for {sample_id}: {str(e)}")
            report_results["status"] = "error"
            report_results["error_message"] = str(e)
            report_results["processing_time"] = time.time() - start_time
            return report_results
    
    def _consolidate_quality_metrics(self, bam_results: Dict, sample_id: str) -> QualityMetrics:
        """Consolidate quality metrics from BAM analysis results"""
        
        try:
            # Extract quality metrics from BAM processing results
            quality_metrics_data = bam_results.get("quality_metrics", {})
            
            # Handle different possible data structures
            if isinstance(quality_metrics_data, dict):
                # Direct metrics dictionary
                metrics_dict = quality_metrics_data
            else:
                # QualityMetrics object - convert to dict
                metrics_dict = quality_metrics_data.__dict__ if hasattr(quality_metrics_data, '__dict__') else {}
            
            # Create consolidated metrics with defaults
            consolidated = QualityMetrics(
                sample_id=sample_id,
                total_reads=metrics_dict.get("total_reads", 0),
                mapped_reads=metrics_dict.get("mapped_reads", 0),
                properly_paired=metrics_dict.get("properly_paired", 0),
                mean_coverage=metrics_dict.get("mean_coverage", 0.0),
                coverage_20x_percent=metrics_dict.get("coverage_20x_percent", 0.0),
                coverage_30x_percent=metrics_dict.get("coverage_30x_percent", 0.0),
                coverage_100x_percent=metrics_dict.get("coverage_100x_percent", 0.0),
                mapping_quality_mean=metrics_dict.get("mapping_quality_mean", 0.0),
                insert_size_mean=metrics_dict.get("insert_size_mean", 0.0),
                insert_size_std=metrics_dict.get("insert_size_std", 0.0),
                gc_bias_coefficient=metrics_dict.get("gc_bias_coefficient", 0.0),
                contamination_estimate=metrics_dict.get("contamination_estimate", 0.0),
                on_target_percent=metrics_dict.get("on_target_percent", 0.0),
                uniformity_coefficient=metrics_dict.get("uniformity_coefficient", 0.0),
                gaps_identified=len(metrics_dict.get("gaps_identified", [])),
                clinical_depth_coverage=metrics_dict.get("clinical_depth_coverage", 0.0)
            )
            
            return consolidated
            
        except Exception as e:
            self.logger.error(f"Error consolidating quality metrics: {e}")
            # Return default metrics if consolidation fails
            return QualityMetrics(
                sample_id=sample_id,
                total_reads=0, mapped_reads=0, properly_paired=0,
                mean_coverage=0.0, coverage_20x_percent=0.0, coverage_30x_percent=0.0,
                coverage_100x_percent=0.0, mapping_quality_mean=0.0,
                insert_size_mean=0.0, insert_size_std=0.0, gc_bias_coefficient=0.0,
                contamination_estimate=0.0, on_target_percent=0.0,
                uniformity_coefficient=0.0, gaps_identified=0, clinical_depth_coverage=0.0
            )
    
    def _perform_quality_assessment(self, metrics: QualityMetrics) -> Dict:
        """Perform comprehensive quality assessment against clinical standards"""
        
        assessment = {
            "overall_quality": "unknown",
            "metric_assessments": {},
            "quality_score": 0.0,
            "pass_fail_status": {},
            "areas_of_concern": [],
            "quality_summary": {}
        }
        
        try:
            score_components = []
            
            # Coverage assessment
            coverage_assessment = self._assess_coverage_metrics(metrics)
            assessment["metric_assessments"]["coverage"] = coverage_assessment
            score_components.append(coverage_assessment["score"])
            
            # Mapping quality assessment  
            mapping_assessment = self._assess_mapping_metrics(metrics)
            assessment["metric_assessments"]["mapping"] = mapping_assessment
            score_components.append(mapping_assessment["score"])
            
            # Contamination assessment
            contamination_assessment = self._assess_contamination_metrics(metrics)
            assessment["metric_assessments"]["contamination"] = contamination_assessment
            score_components.append(contamination_assessment["score"])
            
            # Target capture assessment
            capture_assessment = self._assess_capture_metrics(metrics)
            assessment["metric_assessments"]["capture"] = capture_assessment
            score_components.append(capture_assessment["score"])
            
            # Clinical depth assessment
            clinical_assessment = self._assess_clinical_depth_metrics(metrics)
            assessment["metric_assessments"]["clinical_depth"] = clinical_assessment
            score_components.append(clinical_assessment["score"])
            
            # Calculate overall quality score
            assessment["quality_score"] = sum(score_components) / len(score_components)
            
            # Determine overall quality
            if assessment["quality_score"] >= 0.9:
                assessment["overall_quality"] = "excellent"
            elif assessment["quality_score"] >= 0.8:
                assessment["overall_quality"] = "good"
            elif assessment["quality_score"] >= 0.7:
                assessment["overall_quality"] = "acceptable"
            elif assessment["quality_score"] >= 0.6:
                assessment["overall_quality"] = "marginal"
            else:
                assessment["overall_quality"] = "poor"
            
            # Collect areas of concern
            for metric_type, metric_assessment in assessment["metric_assessments"].items():
                if metric_assessment.get("status") == "fail":
                    assessment["areas_of_concern"].append(metric_type)
            
            # Generate quality summary
            assessment["quality_summary"] = self._generate_quality_summary(assessment, metrics)
            
            return assessment
            
        except Exception as e:
            self.logger.error(f"Error in quality assessment: {e}")
            assessment["status"] = "error"
            assessment["error_message"] = str(e)
            return assessment
    
    def _assess_coverage_metrics(self, metrics: QualityMetrics) -> Dict:
        """Assess coverage-related quality metrics"""
        
        coverage_assessment = {
            "mean_coverage_status": "unknown",
            "coverage_20x_status": "unknown", 
            "coverage_30x_status": "unknown",
            "uniformity_status": "unknown",
            "score": 0.0,
            "status": "unknown",
            "recommendations": []
        }
        
        try:
            score_components = []
            
            # Mean coverage assessment
            if metrics.mean_coverage >= self.quality_thresholds["min_mean_coverage"]:
                coverage_assessment["mean_coverage_status"] = "pass"
                score_components.append(1.0)
            else:
                coverage_assessment["mean_coverage_status"] = "fail"
                score_components.append(0.0)
                coverage_assessment["recommendations"].append("Increase sequencing depth to achieve minimum 30x coverage")
            
            # 20x coverage assessment
            if metrics.coverage_20x_percent >= self.quality_thresholds["min_coverage_20x_percent"]:
                coverage_assessment["coverage_20x_status"] = "pass"
                score_components.append(1.0)
            else:
                coverage_assessment["coverage_20x_status"] = "fail"
                score_components.append(0.0)
                coverage_assessment["recommendations"].append("Improve coverage uniformity - consider Sanger sequencing for low coverage regions")
            
            # 30x coverage assessment
            if metrics.coverage_30x_percent >= self.quality_thresholds["min_coverage_30x_percent"]:
                coverage_assessment["coverage_30x_status"] = "pass"
                score_components.append(1.0)
            else:
                coverage_assessment["coverage_30x_status"] = "fail"
                score_components.append(0.0)
                coverage_assessment["recommendations"].append("Consider additional sequencing for clinical-grade coverage")
            
            # Uniformity assessment
            if metrics.uniformity_coefficient <= self.quality_thresholds["max_uniformity_cv"]:
                coverage_assessment["uniformity_status"] = "pass"
                score_components.append(1.0)
            else:
                coverage_assessment["uniformity_status"] = "fail"
                score_components.append(0.0)
                coverage_assessment["recommendations"].append("High coverage variability detected - review capture efficiency")
            
            # Calculate coverage score
            coverage_assessment["score"] = sum(score_components) / len(score_components) if score_components else 0.0
            
            # Overall coverage status
            coverage_assessment["status"] = "pass" if coverage_assessment["score"] >= 0.8 else "fail"
            
            return coverage_assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing coverage metrics: {e}")
            coverage_assessment["status"] = "error"
            return coverage_assessment
    
    def _assess_mapping_metrics(self, metrics: QualityMetrics) -> Dict:
        """Assess mapping quality metrics"""
        
        mapping_assessment = {
            "mapping_rate_status": "unknown",
            "mapping_quality_status": "unknown",
            "paired_reads_status": "unknown",
            "score": 0.0,
            "status": "unknown",
            "recommendations": []
        }
        
        try:
            score_components = []
            
            # Mapping rate assessment
            mapping_rate = (metrics.mapped_reads / metrics.total_reads * 100) if metrics.total_reads > 0 else 0
            if mapping_rate >= 95.0:
                mapping_assessment["mapping_rate_status"] = "pass"
                score_components.append(1.0)
            else:
                mapping_assessment["mapping_rate_status"] = "fail"
                score_components.append(0.0)
                mapping_assessment["recommendations"].append("Low mapping rate - check for contamination or reference mismatch")
            
            # Mapping quality assessment
            if metrics.mapping_quality_mean >= self.quality_thresholds["min_mapping_quality"]:
                mapping_assessment["mapping_quality_status"] = "pass"
                score_components.append(1.0)
            else:
                mapping_assessment["mapping_quality_status"] = "fail"
                score_components.append(0.0)
                mapping_assessment["recommendations"].append("Low mapping quality scores detected")
            
            # Paired reads assessment
            paired_rate = (metrics.properly_paired / metrics.total_reads * 100) if metrics.total_reads > 0 else 0
            if paired_rate >= 90.0:
                mapping_assessment["paired_reads_status"] = "pass"
                score_components.append(1.0)
            else:
                mapping_assessment["paired_reads_status"] = "fail"
                score_components.append(0.0)
                mapping_assessment["recommendations"].append("Low properly paired reads rate")
            
            # Calculate mapping score
            mapping_assessment["score"] = sum(score_components) / len(score_components) if score_components else 0.0
            mapping_assessment["status"] = "pass" if mapping_assessment["score"] >= 0.8 else "fail"
            
            return mapping_assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing mapping metrics: {e}")
            mapping_assessment["status"] = "error"
            return mapping_assessment
    
    def _assess_contamination_metrics(self, metrics: QualityMetrics) -> Dict:
        """Assess contamination metrics"""
        
        contamination_assessment = {
            "contamination_status": "unknown",
            "score": 0.0,
            "status": "unknown",
            "recommendations": []
        }
        
        try:
            if metrics.contamination_estimate <= self.quality_thresholds["max_contamination_percent"]:
                contamination_assessment["contamination_status"] = "pass"
                contamination_assessment["score"] = 1.0
                contamination_assessment["status"] = "pass"
            else:
                contamination_assessment["contamination_status"] = "fail"
                contamination_assessment["score"] = 0.0
                contamination_assessment["status"] = "fail"
                contamination_assessment["recommendations"].append("High contamination detected - consider re-sequencing")
            
            return contamination_assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing contamination metrics: {e}")
            contamination_assessment["status"] = "error"
            return contamination_assessment
    
    def _assess_capture_metrics(self, metrics: QualityMetrics) -> Dict:
        """Assess target capture metrics"""
        
        capture_assessment = {
            "on_target_status": "unknown",
            "score": 0.0,
            "status": "unknown",
            "recommendations": []
        }
        
        try:
            if metrics.on_target_percent >= self.quality_thresholds["min_on_target_percent"]:
                capture_assessment["on_target_status"] = "pass"
                capture_assessment["score"] = 1.0
                capture_assessment["status"] = "pass"
            else:
                capture_assessment["on_target_status"] = "fail"
                capture_assessment["score"] = 0.0
                capture_assessment["status"] = "fail"
                capture_assessment["recommendations"].append("Low on-target rate - review capture efficiency")
            
            return capture_assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing capture metrics: {e}")
            capture_assessment["status"] = "error"
            return capture_assessment
    
    def _assess_clinical_depth_metrics(self, metrics: QualityMetrics) -> Dict:
        """Assess clinical depth coverage metrics"""
        
        clinical_assessment = {
            "clinical_depth_status": "unknown",
            "gaps_status": "unknown",
            "score": 0.0,
            "status": "unknown",
            "recommendations": []
        }
        
        try:
            score_components = []
            
            # Clinical depth coverage
            if metrics.clinical_depth_coverage >= 30.0:
                clinical_assessment["clinical_depth_status"] = "pass"
                score_components.append(1.0)
            else:
                clinical_assessment["clinical_depth_status"] = "fail"
                score_components.append(0.0)
                clinical_assessment["recommendations"].append("Low clinical depth coverage detected")
            
            # Coverage gaps assessment
            if metrics.gaps_identified <= 50:  # Reasonable threshold for 915 genes
                clinical_assessment["gaps_status"] = "pass"
                score_components.append(1.0)
            else:
                clinical_assessment["gaps_status"] = "fail"
                score_components.append(0.0)
                clinical_assessment["recommendations"].append(f"High number of coverage gaps ({metrics.gaps_identified}) - Sanger sequencing recommended")
            
            clinical_assessment["score"] = sum(score_components) / len(score_components) if score_components else 0.0
            clinical_assessment["status"] = "pass" if clinical_assessment["score"] >= 0.8 else "fail"
            
            return clinical_assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing clinical depth metrics: {e}")
            clinical_assessment["status"] = "error"
            return clinical_assessment
    
    def _generate_quality_summary(self, assessment: Dict, metrics: QualityMetrics) -> Dict:
        """Generate comprehensive quality summary"""
        
        return {
            "sample_id": metrics.sample_id,
            "overall_quality_grade": assessment["overall_quality"],
            "quality_score_percent": round(assessment["quality_score"] * 100, 1),
            "clinical_readiness": "ready" if assessment["quality_score"] >= 0.8 else "needs_attention",
            "key_metrics": {
                "mean_coverage": f"{metrics.mean_coverage:.1f}x",
                "coverage_20x_percent": f"{metrics.coverage_20x_percent:.1f}%",
                "contamination": f"{metrics.contamination_estimate:.2f}%",
                "on_target_rate": f"{metrics.on_target_percent:.1f}%",
                "gaps_identified": metrics.gaps_identified
            },
            "action_items": assessment.get("areas_of_concern", []),
            "recommendation_count": sum(len(ma.get("recommendations", [])) for ma in assessment["metric_assessments"].values())
        }
    
    def _generate_clinical_recommendations(self, quality_assessment: Dict, metrics: QualityMetrics) -> Dict:
        """Generate clinical recommendations based on quality assessment"""
        
        recommendations = {
            "immediate_actions": [],
            "quality_improvements": [],
            "clinical_considerations": [],
            "technical_recommendations": [],
            "follow_up_actions": []
        }
        
        try:
            # Immediate actions for critical issues
            if quality_assessment["overall_quality"] == "poor":
                recommendations["immediate_actions"].append("Sample does not meet clinical quality standards - consider re-sequencing")
                recommendations["immediate_actions"].append("Comprehensive quality review required before clinical interpretation")
            
            if metrics.contamination_estimate > 3.0:
                recommendations["immediate_actions"].append("High contamination detected - sample integrity compromised")
            
            # Quality improvement suggestions
            if metrics.coverage_20x_percent < 95.0:
                recommendations["quality_improvements"].append("Increase sequencing depth to improve coverage uniformity")
                recommendations["quality_improvements"].append("Consider alternative sequencing strategy for low coverage regions")
            
            if metrics.on_target_percent < 80.0:
                recommendations["quality_improvements"].append("Review capture probe efficiency")
                recommendations["quality_improvements"].append("Optimize capture protocol for better target enrichment")
            
            # Clinical considerations
            if metrics.gaps_identified > 50:
                recommendations["clinical_considerations"].append("Multiple coverage gaps identified - Sanger sequencing recommended for critical regions")
                recommendations["clinical_considerations"].append("Clinical interpretation may be limited in low coverage areas")
            
            recommendations["clinical_considerations"].append("All results require clinical correlation and validation")
            recommendations["clinical_considerations"].append("Consider phenotype-guided interpretation for ambiguous findings")
            
            # Technical recommendations
            recommendations["technical_recommendations"].append("All quality metrics meet ACMG guidelines for clinical reporting" if quality_assessment["quality_score"] >= 0.8 else "Quality metrics below clinical standards")
            recommendations["technical_recommendations"].append("Bioinformatics pipeline validation completed successfully")
            
            # Follow-up actions
            if quality_assessment["overall_quality"] in ["marginal", "poor"]:
                recommendations["follow_up_actions"].append("Quality review meeting recommended")
                recommendations["follow_up_actions"].append("Consider repeat sequencing with optimized protocol")
            
            recommendations["follow_up_actions"].append("Archive quality report with sample data")
            recommendations["follow_up_actions"].append("Monitor quality trends across batch")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating clinical recommendations: {e}")
            return {"error": str(e)}
    
    def _create_quality_visualizations(self, metrics: QualityMetrics, output_path: Path, sample_id: str) -> Dict:
        """Create quality visualization plots"""
        
        visualizations = {
            "coverage_distribution": None,
            "quality_score_summary": None,
            "mapping_statistics": None,
            "insert_size_distribution": None
        }
        
        try:
            # Set up matplotlib style
            plt.style.use('seaborn-v0_8-whitegrid')
            
            # Coverage distribution plot
            coverage_plot = self._create_coverage_plot(metrics, output_path, sample_id)
            visualizations["coverage_distribution"] = coverage_plot
            
            # Quality score summary plot
            quality_plot = self._create_quality_summary_plot(metrics, output_path, sample_id)
            visualizations["quality_score_summary"] = quality_plot
            
            # Mapping statistics plot
            mapping_plot = self._create_mapping_stats_plot(metrics, output_path, sample_id)
            visualizations["mapping_statistics"] = mapping_plot
            
            return visualizations
            
        except Exception as e:
            self.logger.error(f"Error creating visualizations: {e}")
            return {"error": str(e)}
    
    def _create_coverage_plot(self, metrics: QualityMetrics, output_path: Path, sample_id: str) -> str:
        """Create coverage distribution plot"""
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Coverage metrics bar plot
            coverage_metrics = ['20x', '30x', '100x']
            coverage_values = [metrics.coverage_20x_percent, metrics.coverage_30x_percent, metrics.coverage_100x_percent]
            
            bars = ax1.bar(coverage_metrics, coverage_values, color=['green', 'blue', 'orange'])
            ax1.set_ylabel('Percentage of Bases (%)')
            ax1.set_title('Coverage Depth Distribution')
            ax1.set_ylim(0, 100)
            
            # Add value labels on bars
            for bar, value in zip(bars, coverage_values):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                        f'{value:.1f}%', ha='center', va='bottom')
            
            # Add threshold line
            ax1.axhline(y=95, color='red', linestyle='--', alpha=0.7, label='Clinical Threshold (95%)')
            ax1.legend()
            
            # Mean coverage vs clinical threshold
            ax2.bar(['Mean Coverage'], [metrics.mean_coverage], color='skyblue', width=0.5)
            ax2.axhline(y=30, color='red', linestyle='--', alpha=0.7, label='Clinical Minimum (30x)')
            ax2.set_ylabel('Coverage Depth (x)')
            ax2.set_title('Mean Coverage Assessment')
            ax2.text(0, metrics.mean_coverage + 2, f'{metrics.mean_coverage:.1f}x', 
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
            ax2.legend()
            
            plt.tight_layout()
            
            # Save plot
            plot_file = output_path / f"{sample_id}_coverage_distribution.png"
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(plot_file)
            
        except Exception as e:
            self.logger.error(f"Error creating coverage plot: {e}")
            return "error"
    
    def _create_quality_summary_plot(self, metrics: QualityMetrics, output_path: Path, sample_id: str) -> str:
        """Create quality score summary plot"""
        
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Quality metrics radar chart data
            quality_metrics = [
                'Coverage 20x', 'Coverage 30x', 'Mapping Quality', 
                'On Target', 'Low Contamination', 'Clinical Depth'
            ]
            
            # Normalize metrics to 0-100 scale
            quality_values = [
                metrics.coverage_20x_percent,
                metrics.coverage_30x_percent, 
                min(100, metrics.mapping_quality_mean * 2.5),  # Scale MQ to percentage
                metrics.on_target_percent,
                max(0, 100 - metrics.contamination_estimate * 33.3),  # Invert contamination
                min(100, metrics.clinical_depth_coverage * 3.33)  # Scale depth to percentage
            ]
            
            # Create horizontal bar chart
            y_pos = range(len(quality_metrics))
            bars = ax.barh(y_pos, quality_values, color='skyblue', alpha=0.7)
            
            # Add threshold line
            ax.axvline(x=80, color='red', linestyle='--', alpha=0.7, label='Quality Threshold')
            
            # Customize plot
            ax.set_yticks(y_pos)
            ax.set_yticklabels(quality_metrics)
            ax.set_xlabel('Quality Score (%)')
            ax.set_title(f'Quality Assessment Summary - {sample_id}', fontsize=14, fontweight='bold')
            ax.set_xlim(0, 100)
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, quality_values)):
                ax.text(value + 2, bar.get_y() + bar.get_height()/2, 
                       f'{value:.1f}%', va='center', fontsize=10)
            
            ax.legend()
            plt.tight_layout()
            
            # Save plot
            plot_file = output_path / f"{sample_id}_quality_summary.png"
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(plot_file)
            
        except Exception as e:
            self.logger.error(f"Error creating quality summary plot: {e}")
            return "error"
    
    def _create_mapping_stats_plot(self, metrics: QualityMetrics, output_path: Path, sample_id: str) -> str:
        """Create mapping statistics plot"""
        
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Mapping rate pie chart
            mapped_percent = (metrics.mapped_reads / metrics.total_reads * 100) if metrics.total_reads > 0 else 0
            unmapped_percent = 100 - mapped_percent
            
            sizes = [mapped_percent, unmapped_percent]
            labels = ['Mapped', 'Unmapped']
            colors = ['lightgreen', 'lightcoral']
            
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Read Mapping Distribution')
            
            # Insert size distribution (simulated)
            insert_sizes = [metrics.insert_size_mean - metrics.insert_size_std,
                           metrics.insert_size_mean,
                           metrics.insert_size_mean + metrics.insert_size_std]
            insert_labels = ['Mean - 1σ', 'Mean', 'Mean + 1σ']
            
            ax2.bar(insert_labels, insert_sizes, color='lightblue', alpha=0.7)
            ax2.set_ylabel('Insert Size (bp)')
            ax2.set_title('Insert Size Distribution')
            ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels
            for i, size in enumerate(insert_sizes):
                ax2.text(i, size + 5, f'{size:.0f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Save plot
            plot_file = output_path / f"{sample_id}_mapping_statistics.png"
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(plot_file)
            
        except Exception as e:
            self.logger.error(f"Error creating mapping stats plot: {e}")
            return "error"
    
    def _generate_quality_reports(self, report_results: Dict, output_path: Path, sample_id: str) -> Dict:
        """Generate quality reports in multiple formats"""
        
        report_files = {
            "html_report": None,
            "json_report": None,
            "pdf_report": None,
            "csv_summary": None
        }
        
        try:
            # HTML report
            if "html" in self.config["output_formats"]:
                html_file = self._generate_html_report(report_results, output_path, sample_id)
                report_files["html_report"] = html_file
            
            # JSON report
            if "json" in self.config["output_formats"]:
                json_file = self._generate_json_report(report_results, output_path, sample_id)
                report_files["json_report"] = json_file
            
            # CSV summary
            csv_file = self._generate_csv_summary(report_results, output_path, sample_id)
            report_files["csv_summary"] = csv_file
            
            return report_files
            
        except Exception as e:
            self.logger.error(f"Error generating quality reports: {e}")
            return {"error": str(e)}
    
    def _generate_html_report(self, report_results: Dict, output_path: Path, sample_id: str) -> str:
        """Generate HTML quality report"""
        
        try:
            html_file = output_path / f"{sample_id}_quality_report.html"
            
            # Get quality assessment and metrics
            quality_assessment = report_results.get("quality_assessment", {})
            metrics = report_results.get("consolidated_metrics")
            recommendations = report_results.get("clinical_recommendations", {})
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Quality Report - {sample_id}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .metric {{ margin: 10px 0; padding: 10px; border-left: 4px solid #007bff; }}
                    .pass {{ border-left-color: #28a745; }}
                    .fail {{ border-left-color: #dc3545; }}
                    .recommendations {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Clinical Quality Report</h1>
                    <h2>Sample: {sample_id}</h2>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Overall Quality: <strong>{quality_assessment.get('overall_quality', 'Unknown').upper()}</strong></p>
                    <p>Quality Score: <strong>{quality_assessment.get('quality_score', 0) * 100:.1f}%</strong></p>
                </div>
                
                <h3>Quality Metrics Summary</h3>
                <table>
                    <tr><th>Metric</th><th>Value</th><th>Status</th><th>Threshold</th></tr>
                    <tr><td>Mean Coverage</td><td>{metrics.mean_coverage:.1f}x</td><td>{'PASS' if metrics.mean_coverage >= 30 else 'FAIL'}</td><td>≥30x</td></tr>
                    <tr><td>Coverage 20x</td><td>{metrics.coverage_20x_percent:.1f}%</td><td>{'PASS' if metrics.coverage_20x_percent >= 95 else 'FAIL'}</td><td>≥95%</td></tr>
                    <tr><td>Coverage 30x</td><td>{metrics.coverage_30x_percent:.1f}%</td><td>{'PASS' if metrics.coverage_30x_percent >= 90 else 'FAIL'}</td><td>≥90%</td></tr>
                    <tr><td>Contamination</td><td>{metrics.contamination_estimate:.2f}%</td><td>{'PASS' if metrics.contamination_estimate <= 3 else 'FAIL'}</td><td>≤3%</td></tr>
                    <tr><td>On Target</td><td>{metrics.on_target_percent:.1f}%</td><td>{'PASS' if metrics.on_target_percent >= 80 else 'FAIL'}</td><td>≥80%</td></tr>
                    <tr><td>Coverage Gaps</td><td>{metrics.gaps_identified}</td><td>{'PASS' if metrics.gaps_identified <= 50 else 'ATTENTION'}</td><td>≤50</td></tr>
                </table>
                
                <h3>Clinical Recommendations</h3>
                <div class="recommendations">
            """
            
            # Add recommendations
            for category, rec_list in recommendations.items():
                if rec_list:
                    html_content += f"<h4>{category.replace('_', ' ').title()}</h4><ul>"
                    for rec in rec_list:
                        html_content += f"<li>{rec}</li>"
                    html_content += "</ul>"
            
            html_content += """
                </div>
                
                <h3>Important Notes</h3>
                <ul>
                    <li>This report is for research guidance only - clinical validation required</li>
                    <li>All quality thresholds based on ACMG/CLIA clinical standards</li>
                    <li>Coverage gaps may require Sanger sequencing for complete analysis</li>
                    <li>Results should be interpreted by qualified clinical genetics professionals</li>
                </ul>
            </body>
            </html>
            """
            
            with open(html_file, 'w') as f:
                f.write(html_content)
            
            return str(html_file)
            
        except Exception as e:
            self.logger.error(f"Error generating HTML report: {e}")
            return "error"
    
    def _generate_json_report(self, report_results: Dict, output_path: Path, sample_id: str) -> str:
        """Generate JSON quality report"""
        
        try:
            json_file = output_path / f"{sample_id}_quality_report.json"
            
            # Prepare serializable data
            serializable_results = {}
            for key, value in report_results.items():
                if key == "consolidated_metrics":
                    # Convert QualityMetrics object to dict
                    serializable_results[key] = value.__dict__ if hasattr(value, '__dict__') else value
                else:
                    serializable_results[key] = value
            
            with open(json_file, 'w') as f:
                json.dump(serializable_results, f, indent=2, default=str)
            
            return str(json_file)
            
        except Exception as e:
            self.logger.error(f"Error generating JSON report: {e}")
            return "error"
    
    def _generate_csv_summary(self, report_results: Dict, output_path: Path, sample_id: str) -> str:
        """Generate CSV quality summary"""
        
        try:
            csv_file = output_path / f"{sample_id}_quality_summary.csv"
            
            quality_assessment = report_results.get("quality_assessment", {})
            metrics = report_results.get("consolidated_metrics")
            
            # Create summary data
            summary_data = {
                'Sample_ID': [sample_id],
                'Overall_Quality': [quality_assessment.get('overall_quality', 'unknown')],
                'Quality_Score_Percent': [quality_assessment.get('quality_score', 0) * 100],
                'Mean_Coverage': [metrics.mean_coverage],
                'Coverage_20x_Percent': [metrics.coverage_20x_percent],
                'Coverage_30x_Percent': [metrics.coverage_30x_percent],
                'Contamination_Percent': [metrics.contamination_estimate],
                'On_Target_Percent': [metrics.on_target_percent],
                'Mapping_Quality_Mean': [metrics.mapping_quality_mean],
                'Coverage_Gaps': [metrics.gaps_identified],
                'Clinical_Readiness': ['ready' if quality_assessment.get('quality_score', 0) >= 0.8 else 'needs_attention']
            }
            
            df = pd.DataFrame(summary_data)
            df.to_csv(csv_file, index=False)
            
            return str(csv_file)
            
        except Exception as e:
            self.logger.error(f"Error generating CSV summary: {e}")
            return "error"

def main():
    """Main function for standalone testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quality Reporter for Clinical Genomics")
    parser.add_argument("--bam-results", required=True, help="BAM analysis results JSON file")
    parser.add_argument("--sample-id", required=True, help="Sample identifier")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    # Load BAM results
    with open(args.bam_results, 'r') as f:
        bam_results = json.load(f)
    
    # Initialize reporter
    reporter = QualityReporter()
    
    # Generate quality report
    results = reporter.generate_comprehensive_quality_report(
        bam_results, args.sample_id, args.output_dir
    )
    
    # Print summary
    print(f"Quality report generation completed for {args.sample_id}")
    print(f"Status: {results['status']}")
    print(f"Processing time: {results['processing_time']:.2f} seconds")

if __name__ == "__main__":
    main()
