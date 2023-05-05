# Development Info

The goal of this document is to collect some general info on how this project was developed to ease in reuse of the code.

Thoughts:
- The code was broken up with two mixins to encapsulate the Dataset/Dataverse field setting and confirming. The page navigation and assertions around that are covered by `test_ingest_workflow_report.py`, with the goal of making more of the navigation+assertions modular as development expands.
- The tests in `test_ingest_workflow_report.py` were designed to be run linearly and will break if run out of order. You may be able to disable r06 & r07 (template creation) as those don't majorly impact the future tests.
- Most of the scrolling in the code is for screenshot purposes, but some is done to get elements on-screen for interaction to work.
