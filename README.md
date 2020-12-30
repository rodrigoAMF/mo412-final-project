# MO412 - Algoritmos em Grafos - Final Research Project

In the final project students are asked to select a network of interest to them, map it out and analyze it. The purpose of the final project is to test a student's ability to analyze a network. Consequently students must stay focused on exploring the network aspect of the data, and avoid being carried away by other tempting questions their dataset poses that would take them away from this goal

Each group has 10 minutes to present their final project. Time limit is strictly enforced. On the first slide, give your title, name and program.

Tell us about your data and the data collection method. Show an entry of the data source to offer a sense of where you started from.

Measure: N, L, and their time dependence if you have a time dependent network; degree distribution, average path length, clustering coefficient, C(k), the weight distribution P(w) if you have a weighted network. Visualize communities: discuss network robustness and spreading, degree correlations, whichever is appropriate for your project. 

It is not sufficient to simply measure things you - you need to discuss the insights you gained, always asking:
* Whats was your expectation?
* What is the proper random reference?
* How do the results compare to your expectation?
* What did you learn form each quantity?

Grading criteria:
* Use of network tools(completeness/correctness);
* Ability to extract information/insights from your data using the network tools
* Overall quality of the project/presentation

**No need to write a report - email us the presentation as a pdf file** (need to confirm with professor)

## Environment setup
Install [anaconda](https://www.anaconda.com/products/individual) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) clone this project, open repository main folder in a terminal and run:

```
conda create -n MO412 python=3.8.5
conda activate MO412
pip install -r requirements.txt
```

## Project package setup
Open repository main folder in a terminal and run:

```
cd project
pip install -e .
```
