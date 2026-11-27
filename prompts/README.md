# prompts

One file per prompt, with the version in the file name: `<name>.v<n>.md`, for example `extract_concepts.v1.md`.

Never edit a released version in place. Add `v<n+1>`, run the stage's eval (`make eval STAGE=<stage>`), and report before → after in the PR.
