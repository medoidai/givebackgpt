name: 🌟 Feature Request
description: Create a feature request.
title: '[FEATURE]: '
type: 'Feature'
labels: ['enhancement']

body:
  - type: textarea
    id: summary
    attributes:
      label: Summary
      description: "A clear and concise summary of the feature you're requesting."
    validations:
      required: true

  - type: textarea
    id: detailed_description
    attributes:
      label: Detailed Description
      description: "A more comprehensive explanation of the feature, including how it would work, its benefits, and why it's needed."
    validations:
      required: true

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: "What is the priority of the feature?"
      options:
        - "High: Critical for project success"
        - "Medium: Useful, but not urgent"
        - "Low: Nice-to-have feature"
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives
      description: "If you have any alternative solutions or features you've considered, please add them."
    validations:
      required: false

  - type: textarea
    id: additional_notes
    attributes:
      label: Additional Notes
      description: "If you have any additional information regarding the feature, please add them."
    validations:
      required: false

  - type: textarea
    id: related_issues
    attributes:
      label: Related Issues
      description: "If you have any related issues regarding the feature, please link them. The hashtag (#) is used to mention issues by their unique number, such as #123."
    validations:
      required: false