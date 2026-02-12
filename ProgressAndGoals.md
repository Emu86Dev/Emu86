# Progress and Goals


## Progress
Frontend:
- Updated the overall color theme
- Resized the CodeMirror
- Updated the logo
- Updated the styling for buttons / selections
- Updated the styling of texts
- Adjusted button color and border to fit Matt's design
- Solved different rendering of registers block across different browsers

Backend:
- Re-architected backend routing: replaced `/main` with slug-based URL (`/<flavor>-<base>`) to solve the refresh page failure
- Implemented CI/CD pipeline with automated tests that deploys to PythonAnywhere
- Added flake8 and django-template-check
- Fixed numerous uncaught runtime page crashes
- Added emulator selection feature to the emulation page
- Fixed step function not stopping after main function execution
- Fixed selected program not persisting after run/step 


## Goal

Frontend:
- Add show/hide toggle to registers section and error section
- Redesign & update the UI for Feedback page
- Fix legacy linting errors detected by template check


Backend:
- Bring back WASM features
- Test and revive Jupyter Notebook capabilities
- Add uploading local program feature
- Reset Registers after program selection
- Optimization
  - Convert Run/Step/Clear to AJAX calls with JSON responses (partial rendering)
  - Move VM state to Django sessions (avoid round-tripping all state in form data)

