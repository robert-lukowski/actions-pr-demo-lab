# GitHub Actions Pull Request Lab

This repository contains a private, fake GitHub Actions lab for testing pull request automation against sample OpenAPI schema files.

## Testing The Workflow

1. Create the `release` branch from `main`.
2. Push both `main` and `release` to GitHub.
3. Make sure repository settings allow GitHub Actions to create pull requests:
   - Settings -> Actions -> General -> Workflow permissions -> Read and write permissions
   - Enable "Allow GitHub Actions to create and approve pull requests" if available.
4. Run the `Prepare Release Paths PR` workflow manually from the Actions tab.
5. Confirm the expected pull request diff only changes:

```diff
-  /demo-api:
+  /release-api:
```

The server URL, title, description, and other metadata should remain unchanged.
