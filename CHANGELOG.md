# Changelog

## [1.3.0] 2025-06-14

### Added
- Implemented live Markdown and LaTeX preview in `edit-post.html`.
- Added support for image uploads and image URLs in post editor.
- Enabled profile image upload during account creation and profile updates.
- Enabled inline LaTeX math expressions using `$...$` syntax.
- Display images in posts with improved CSS styling.

### Changed
- Redesigned `edit-post.html` structure for better UX and extensibility.
- Adjusted `AboutUs.html` to match the site's theme.
- Set message sync interval in `messenger.html` to 3 seconds.

### Fixed
- Fixed post editing issue in `edit-post.html`.
- Fixed duplicate message issue caused by sync timing.
- Corrected backend URL path integration in frontend.
- Fixed comment date display by parsing server-side date formats and improving formatting consistency.



## [1.2.0] 2025-06-11

### Features
- **admin:** Translated all files in `src/admin` from Arabic to English for consistency and better collaboration. (`feat(admin): translate all files in src/admin to English`)
- **UI Enhancements:**  
  - Introduced dark mode support across the entire site  
  - Improved responsive design for mobile devices  
  - Updated Markdown library to latest version  
  - Enabled LaTeX math rendering in post view  
  (`feat: update UI with dark mode, responsive design improvements, and enhanced Markdown support`)
- **PWA Support:**  
  - Implemented Progressive Web App features including service worker, manifest file, and installation icons  
  - Service worker handles offline caching  
  (`feat: add PWA support with service worker, manifest, and icons`)
- **Caching and Favicon:**  
  - Added all main pages to service worker cache  
  - Set favicon for browser tab display  
  (`feat: add main pages to service worker cache and set favicon`)

### Refactoring
- **APIs:** Translated all API handling modules (`api.js`, `auth.js`) from Arabic to English in both `src/js` and `src/admin/js` directories. Improved naming for readability and maintainability.  
  (`refactor: translate API handling modules to English`)



## [1.1.0]

### Refactored
- Moved all project source files into the `src/` directory for better structure.
- Extracted duplicate CSS rules into `shared_rules.css` in both `admin/css` and `css` directories.
