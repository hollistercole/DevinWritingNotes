# Lessons Learned

This document serves as a collection of best practices, tips, and lessons learned while working on various writing and publishing tasks in this repository. Refer to this document when encountering challenges or starting new tasks.

## GitHub Pages

### Configuration
- **Jekyll Processing**: Adding a `.nojekyll` file to the repository root helps bypass Jekyll processing, which can sometimes cause issues with certain file paths or formats.
- **Path Configuration**: This repository is configured to serve content from the root path (`/`), not from a subdirectory like `/docs`. All content should be placed directly in the repository root to be accessible.
- **Build Time**: GitHub Pages may take several minutes to build and deploy changes after pushing to the repository.

### Content Organization
- **Folder Structure**: Organizing content by task in separate folders helps maintain a clean repository structure and makes navigation easier.
- **Index Files**: Each folder should contain an index.html file to facilitate navigation when accessing the folder URL directly.

## HTML Content

### Best Practices
- **Mobile-First Design**: Design pages with mobile devices as the primary target, then enhance for larger screens. Mobile will be the primary viewing mode for most users.
- **Mobile Responsiveness**: Always include viewport meta tags and responsive CSS to ensure content displays properly on mobile devices.
- **Responsive Layouts**: Use flexible grid layouts, relative units (%, em, rem), and media queries to ensure content adapts to different screen sizes.
- **Touch-Friendly UI**: Make buttons and interactive elements large enough (minimum 44x44px) and properly spaced for touch interaction.
- **Mobile Button Layout**: For navigation buttons on mobile, use `display: block; width: 85%;` with `margin: 0 auto` for centered alignment and consistent vertical spacing (e.g., `margin-bottom: 10px`). Using 85% width instead of 100% creates better visual spacing around buttons.
- **Image Optimization**: Compress images before adding them to the repository to improve page load times.
- **Semantic HTML**: Use proper semantic HTML elements (header, main, footer, etc.) for better accessibility and SEO.

### Testing
- **Mobile Preview**: Test all pages in mobile view using browser developer tools to verify layouts work properly.
- **Responsive Testing**: Check pages at multiple breakpoints to ensure content flows appropriately at all screen sizes.
- **Performance Testing**: Verify that pages load quickly on mobile devices and that images are appropriately sized.

### Common Issues
- **External Resources**: Avoid relying on externally hosted resources (images, CSS, JavaScript) as they may become unavailable or change over time.
- **Path References**: Use relative paths for internal links and resources to ensure they work correctly when the site is deployed.

## Markdown Content

### Formatting Tips
- **Headers**: Use appropriate header levels (# for main title, ## for sections, etc.) to maintain proper document structure.
- **Images**: Include alt text with all images for accessibility: `![Alt text](./images/image.jpg)`
- **Links**: Use descriptive link text rather than generic phrases like "click here": `[Zurich Restaurant Guide](./zurich-restaurants.html)`

### GitHub Flavored Markdown
- **Tables**: Create tables using the pipe syntax for structured data presentation.
- **Task Lists**: Use `- [ ]` and `- [x]` for creating interactive task lists in planning documents.
- **Code Blocks**: Use triple backticks with language specification for syntax highlighting.

## Image Handling

### Storage
- **Local Storage**: Always download and store images locally in an `images` folder within the task directory.
- **Naming Convention**: Use descriptive, kebab-case filenames for images (e.g., `matterhorn-view.jpg`).
- **ImageGrabs Directory**: Use the `/ImageGrabs` directory in the repository root as temporary storage for downloaded/captured images. Images should ultimately be copied to their appropriate organizational location in the hierarchy.

### Downloading Images
- **Unsplash Method**: Use Unsplash.com to find high-quality, freely usable images. Download them directly through the browser and copy them to the appropriate directory.
- **Browser Screenshots**: For images that are difficult to download directly, use browser screenshots to capture the image and save it locally.
- **Attribution**: When using images from sources like Unsplash, include proper attribution in the page footer or in a separate credits section.
- **Reliability**: Always verify downloaded images by checking they appear correctly in the local repository before committing.

### Optimization
- **File Format**: Use JPG for photographs, PNG for graphics with transparency, and SVG for vector graphics.
- **Compression**: Optimize images using tools like TinyPNG or ImageOptim before adding them to the repository.

## Troubleshooting

### Common Issues
- **404 Errors**: If pages return 404 errors after deployment, check the file path and ensure the file exists in the correct location.
- **Broken Links**: Regularly test internal links to ensure they correctly point to existing resources.
- **Display Issues**: Test content on multiple devices and browsers to ensure consistent appearance.

## Communication

### Status Updates
- **Regular Updates**: Provide frequent status updates via Slack, especially when working on longer tasks.
- **Milestone Reporting**: Send updates when reaching key milestones in a task (e.g., "Downloaded all images" or "Completed HTML structure").
- **Screenshots**: Include screenshots of work in progress when relevant to show visual progress.
- **Blockers**: Immediately communicate any blockers or issues that might delay completion.

### Context Awareness
- **Remote Visibility**: Remember that users interacting via Slack cannot see the screen or work in progress unless explicitly shared.
- **Detailed Explanations**: Provide context with each update about what has been done and what's coming next.
- **Links**: Always include direct links to completed work so it can be easily accessed and reviewed.

---

This document will be updated as new lessons are learned and best practices are established. Last updated: April 5, 2025.
