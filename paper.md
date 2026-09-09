---
title: 'NeuroPipe-SABV: An NIH SABV-Compliant Data Processing Pipeline for Preclinical Behavioral Neuroscience'
tags:
  - Python
  - Streamlit
  - behavioral neuroscience
  - sex as a biological variable
  - SABV
  - data pipeline
  - preclinical
authors:
  - name: Kobe Q. Anderson
    orcid: 0009-0006-5464-1323
    affiliation: 1
  - name: Bryan Devan
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: Laboratory for Comparative Neuropsychology, Department of Psychology, Towson University
    index: 1
date: 18 August 2026
bibliography: paper.bib
---

# Summary

Preclinical behavioral neuroscience labs routinely export messy, inconsistent CSV files from video-tracking platforms such as EthoVision XT, ANY-maze, and HVS Image. Cleaning these exports, classifying subjects by sex, checking for artifacts, running statistics, and producing publication-ready figures is tedious, error-prone, and time-consuming, often taking hours per dataset. Additionally, the National Institutes of Health (NIH) now mandates that sex be included as a biological variable (SABV) in all federally funded research. Most laboratories handle SABV compliance manually and inconsistently, using lab-specific Excel templates or ad hoc scripts that are rarely documented or shared.

NeuroPipe-SABV is a free, open-source Streamlit web application that automates the entire workflow from raw export to SABV-compliant analysis. The pipeline standardizes headers across inconsistent export formats, classifies sex automatically from subject identifiers or metadata, detects common tracking artifacts, runs group-comparison and regression statistics, verifies group balance between sexes and conditions, and generates publication-ready visualizations with SABV-compliant reporting. All processing steps are documented, reproducible, and exportable. The application is deployed at https://neuropipesabv.streamlit.app/ and the source code is available at https://github.com/kobeqanderson-png/NeuroPipe-SABV under the MIT license.

# Statement of Need

In 2014, the NIH announced a policy requiring that sex be included as a biological variable in all preclinical research designs, analyses, and reporting [@clayton2014; @mccullough2014; @sandberg2015]. The policy was codified in guide notice NOT-OD-15-102 and remains in effect today. Despite this mandate, compliance in preclinical behavioral neuroscience remains inconsistent. A 2021 review found that fewer than half of published preclinical studies adequately report sex-based analyses, and many still pool male and female data without testing for interaction effects [@shansky2021].

Shansky and Woolley [@shansky2016] argued that considering sex as a biological variable will be valuable for neuroscience research because it will reveal sex-specific mechanisms that are unknown when only one sex is studied. Their argument was a result of subsequent work showing that standard behavioral paradigms and their associated metrics were developed and validated in male rodents, and these metrics may not mean the same thing in females [@shansky2021; @shansky2024]. For example, in fear conditioning, males predominantly freeze while females are more likely to exhibit an escape-like darting response [@shansky2018]. If a study only measures freezing, it will misinterpret female fear learning as poorer performance. This is exactly the kind of interpretational pitfall that SABV compliance is meant to prevent.

Shansky [@shansky2024] has also pointed out that the convergence of the SABV mandate with advancing tracking technology has exposed critical limitations in classic behavioral paradigms. While our tools have advanced, our behavioral metrics have not. Most assays still allow only binary outcomes and were not designed to capture the behavioral diversity that emerges when both sexes are included. This creates a practical problem for labs: even when researchers want to comply with SABV, they lack the infrastructure to analyze sex-disaggregated data properly and report effect sizes that distinguish statistical significance from practical significance.

The root cause is not a lack of statistical knowledge as most behavioral researchers are familiar with t-tests and regression. There is a lack of integrated infrastructure. Video-tracking platforms such as EthoVision XT and ANY-maze export data in vendor-specific CSV formats with inconsistent column names, encoding issues, and missing metadata. Converting these exports into an analysis-ready format, classifying subjects by sex (often inferred from cage-card numbers or subject IDs), checking for tracking artifacts, running the appropriate statistical tests, and producing figures that meet journal and NIH reporting standards typically involves a patchwork of manual Excel manipulation, lab-specific MATLAB or Python scripts, and copy-paste between programs.

There is no existing open-source tool that integrates these steps specifically for SABV compliance in preclinical behavioral neuroscience. General-purpose statistical platforms (e.g., R, SPSS, Prism) require the user to handle data ingestion, cleaning, and sex classification manually. Laboratory information management systems (LIMS) are designed for sample tracking, not behavioral analysis. The realistic alternative to NeuroPipe-SABV is therefore not a named competitor, but the inconsistent manual workflows that dominate the field.

NeuroPipe-SABV addresses this gap by providing a single, guided workflow that is accessible to researchers without programming expertise while remaining fully transparent and extensible for those who do code.

# State of the Field

The current landscape for preclinical behavioral data analysis is fragmented. Most laboratories rely on one of three approaches:

**Manual workflows.** Researchers clean and analyze data in Excel, Prism, or SPSS, copying and pasting between programs. Sex classification is done by hand from cage cards or subject logs. This is the dominant approach and it is error-prone, time-consuming, and rarely documented in a way that permits reproduction.

**General-purpose statistical platforms.** R, Python, SPSS, and Prism can run the necessary statistics, but they require the user to handle data ingestion, cleaning, encoding issues, header standardization, and sex classification manually. None of these platforms include built-in SABV compliance checks or artifact detection tailored to rodent behavioral tracking.

**Laboratory information management systems (LIMS).** These systems are designed for sample tracking, inventory, and experimental logistics, not for behavioral data analysis. They do not ingest video-tracking exports, run statistical tests, or generate publication-ready figures.

Shansky and Murphy [@shansky2021] have argued that incorporating SABV will require a rethinking of how we design and analyze preclinical studies. This rethinking must extend to data analysis infrastructure. If behavioral metrics were developed in males and may not translate directly to females, then researchers need tools that make it easy to analyze sex-disaggregated data, test for interactions, and report effect sizes. Currently, no existing open-source tool integrates data ingestion, header standardization, sex classification, artifact detection, statistical analysis, and SABV-compliant reporting in a single workflow. NeuroPipe-SABV was built to fill this gap rather than extend an existing tool, because no existing tool covers the full pipeline.

# Functionality

NeuroPipe-SABV is organized as a seven-step guided analysis path:

1. Upload Data. Users upload CSV or Excel exports from EthoVision XT, ANY-maze, or other platforms. The ingestion layer attempts UTF-8, Latin-1, and cp1252 decoding to handle cross-platform encoding issues.

2. Process & Classify. The pipeline applies a standardized cleaning routine (strip column names, parse dates, drop duplicates, impute missing numeric values with the median, trim whitespace). Sex classification supports three modes: (a) threshold split on a numeric subject ID (e.g., IDs 1–16 = Male, 17–32 = Female), (b) manual comma-separated ID lists with range support (e.g., "1-16, 20, 22-24"), and (c) female-only list with all others assigned male. The classifier uses a regex-based parser that handles mixed ID formats such as "rat17", "subject_5", and "animal-123".

3. Analyze Differences. The pipeline performs Welch's two-sample t-tests (which do not assume equal variances) and calculates Cohen's d effect sizes for all numeric variables, stratified by sex. Standard error of the mean (SEM) is reported alongside means.

4. Create Visualizations. Distribution plots, boxplots, correlation heatmaps, and scatter plots are generated with matplotlib and seaborn. All figures are styled with a consistent dark theme and can be downloaded as PNG.

5. Build Models. Users can fit linear and polynomial regression models with train/test splitting, feature selection, and residual diagnostics using scikit-learn.

6. Download Results. The full processed dataset, summary statistics, and model outputs can be exported as formatted CSV or Excel workbooks.

7. Data Quality Controls. Throughout the workflow, the pipeline flags tracking artifacts (velocity spikes, frozen coordinates, coordinate jumps, out-of-bounds positions), missing values, and overlapping sex-classification ID lists.

# Design Decisions

Several engineering decisions distinguish NeuroPipe-SABV from a thin wrapper around pandas and scipy:

Header standardization. EthoVision XT and ANY-maze use different column vocabularies for the same measures (e.g., "X center" vs. "Centre point X", "Distance travelled" vs. "Path length").

The pipeline implements a three-tier matching strategy: exact, fuzzy (difflib, 0.85 cutoff), and substring, to map raw column names onto a canonical vocabulary. Collisions (multiple raw columns mapping to the same canonical name) are resolved with suffixed disambiguation. The mapping is extensible at runtime for lab-specific formats.

Sex-classification heuristics. Because many preclinical studies do not record sex explicitly in the tracking export, the pipeline infers it from subject identifiers. The parser handles prefixed labels ("rat17"), delimited labels ("subject_5"), and plain numerics, with vectorized application via pandas `.apply()` for efficiency.

Artifact detection. Rather than relying solely on missing-value counts, the pipeline implements five distinct detectors with rodent-appropriate thresholds: velocity spikes (>2 m/s), tracking dropouts (frozen coordinates for 5+ consecutive frames), coordinate jumps (>0.5 m between frames), missing-value patterns in required columns, and out-of-bounds positions. Detectors are grouped by animal ID to handle multi-subject datasets.

Welch's t-test and Cohen's d. The pipeline defaults to Welch's t-test because it does not assume equal variances which is a common issue in biological data where male and female groups often differ in variance as well as mean. Cohen's d is reported alongside p-values to distinguish statistical significance from practical significance, aligning with current SABV reporting recommendations and with the emphasis Shansky and Murphy [@shansky2021] have placed on proper statistical design for sex-inclusive research.

# Research Impact Statement

NeuroPipe-SABV has been used for behavioral data analysis in the Laboratory for Comparative Neuropsychology at Towson University, including open-field, elevated plus-maze, and Morris water-maze datasets. The pipeline reduces the time required to move from raw export to SABV-compliant analysis from hours to minutes, and it eliminates the manual transcription errors that are common when researchers move data between Excel, Prism, and statistical software. By automating sex classification and SABV reporting, the tool ensures that NIH-mandated analyses are performed consistently across datasets and experiments.

# AI Usage Disclosure

Generative AI was used for code documentation and minimal manuscript drafting assistance. All scientific content was reviewed and verified by the authors.

# Acknowledgements

This work was supported by the Laboratory for Comparative Neuropsychology at Towson University. The authors thank the NIH for public guidance on SABV implementation. The authors have no competing interests to declare.

