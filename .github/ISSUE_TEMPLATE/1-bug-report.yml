name: 🐛 Bug Report
description: Create a bug report.
title: '[BUG]: '
type: 'Bug'
labels: ['bug']

body:
  - type: markdown
    attributes:
      value: |
        ## Bug Details

  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: "A clear and concise summary of what the bug is."
    validations:
      required: true

  - type: textarea
    id: steps_to_reproduce
    attributes:
      label: Steps to Reproduce
      description: "Provide clear, step-by-step instructions to replicate the bug."
    validations:
      required: true

  - type: textarea
    id: expected_behavior
    attributes:
      label: Expected Behavior
      description: "A clear description of what you expected to happen."
    validations:
      required: true

  - type: textarea
    id: actual_behavior
    attributes:
      label: Actual Behavior
      description: "A clear description of what actually happened."
    validations:
      required: true

  - type: dropdown
    id: impact
    attributes:
      label: Impact
      description: "What is the impact of the bug?"
      options:
        - "Critical: Blocks essential functionality or causes system crashes/data loss"
        - "Major: Significantly affects functionality or performance"
        - "High: Impacts important features or causes notable performance issues"
        - "Minor: Causes minor inconvenience, non-blocking issues"
        - "Trivial: Cosmetic issues with no real impact"
    validations:
      required: true

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: "If you have any relevant screenshots to explain the bug, please upload them (e.g., broken layouts, error messages)."
    validations:
      required: false

  - type: textarea
    id: additional_notes
    attributes:
      label: Additional Notes
      description: "If you have any additional information regarding the bug, please add them."
    validations:
      required: false

  - type: textarea
    id: related_issues
    attributes:
      label: Related Issues
      description: "If you have any related issues regarding the bug, please link them. The hashtag (#) is used to mention issues by their unique number, such as #123."
    validations:
      required: false

  - type: markdown
    attributes:
      value: |
        ## Environment

  - type: input
    id: version_tag
    attributes:
      label: Version Tag
      description: "The specific version tag of the software you are using."
      placeholder: "e.g., 1.2.3"
    validations:
      required: false

  - type: input
    id: branch
    attributes:
      label: Branch
      description: "The software branch you are working with."
      placeholder: "e.g., main"
    validations:
      required: false

  - type: input
    id: commit_hash
    attributes:
      label: Commit Hash
      description: "The unique commit hash associated with the version of the software you are using."
      placeholder: "e.g., 24a65c83671b1078c7befefaaf3b6436e257dc99"
    validations:
      required: false

  - type: input
    id: deployment_type
    attributes:
      label: Deployment Type
      description: "The type of deployment environment where the software is running."
      placeholder: "e.g., On-premise, AWS EC2, GCP Cloud Run, Azure App Service"
    validations:
      required: false

  - type: dropdown
    id: environment_type
    attributes:
      label: Environment Type
      description: "The environment in which the software is running."
      options:
        - Development
        - Testing
        - Staging
        - Production
    validations:
      required: false

  - type: input
    id: host_os
    attributes:
      label: Host Operating System
      description: "The operating system running on the host machine where the software is deployed."
      placeholder: "e.g., Ubuntu 22.04, Windows 10, macOS 12"
    validations:
      required: false

  - type: dropdown
    id: reproducibility
    attributes:
      label: Reproducibility
      description: "How often does the bug occur? Choose the frequency to help determine the impact."
      options:
        - "Always: The bug happens every time"
        - "Sometimes: The bug happens intermittently"
        - "Rarely: The bug happens occasionally, but not often"
        - "Cannot Reproduce: The bug cannot be reproduced"
    validations:
      required: false