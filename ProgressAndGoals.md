# Progress and Goals


## Progress
Frontend:
- Updated the overall color theme
- Resized the CodeMirror
- Updated the logo
- Updated the styling for buttons / selections
- Updated the styling of texts
- Adjusted button color and border to fit Matt's design
- Solved different rendering of registers block accross different browser

Backend:
- Re-architected backend routing: utilize slug-based URL to replace `/main`
- Implemented CI/CD pipline that deploy to PythonAnywhere
- Add flake8 and django-template-check

- Fixed numerous uncaught runtime web crashes
- Moved emulator selection to the emulation page
- Prevent step function not stopping after executed main function
- Fixed selected program not persisting after run/step 


## Goal
Frontend:
- Added show/hide toggle to registers section and error section
- Redesign & update the UI for Goals & Feedback page

Backend:
- Bring back WASM features
- Optimization
  - Convert Run/Step/Clear to AJAX calls with JSON responses (partial rendering)
  - Move VM state to Django sessions (avoid round-tripping all state in form data)
