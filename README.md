# Academic Profile Template

Maintain research records in one place and generate a Master CV, a public CV, and a static academic website. The starter example uses a fictional researcher and synthetic results.

## Quick start

1. Select **Use this template** on GitHub. Choose a private repository if it will hold application material or unpublished work.
2. Clone your new repository and create a Python 3.12 or newer virtual environment.
3. Run the build commands below and open `build/public-site/index.html`.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build_profile.py
```

On macOS or Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build_profile.py
```

The build writes `build/Master_CV.pdf`, `build/CV.pdf`, their RenderCV input files, and the static site in `build/public-site/`.

## Make it yours

| File | What to edit |
| --- | --- |
| `profile.yml` | Name, affiliation, bio, education, awards, and activities. Remove `example` once you replace the demonstration content. Optional `website` and `github_url` fields accept full URLs. |
| `projects/` | One Markdown file per project. The ID must match the filename. The body can document contributions, results, and evidence. |
| `publications.yml` | Bibliographic details. An optional `url` links the paper and `code_url` links public code. |
| `cv/selection.yml` | Project and publication IDs to publish. An empty list is valid. |
| `site/assets/` | Site CSS and optional project images. A public project can reference one image filename with alt text and a caption. |

The public CV and homepage use the projects and papers selected in `cv/selection.yml`. Each selected project has a `public` block for its public title, summary, and CV highlights. For a tailored CV, create a separate copy of the generated Master CV YAML and render that version with RenderCV. See [AGENT_BRIEF.md](AGENT_BRIEF.md) for a reusable prompt for application work.

## Publish the site

Preview `build/public-site/`, then publish those files to a separate public website repository. On GitHub Pages, place the files at the root of the publishing branch and configure that branch in **Settings → Pages**. Publishing the separate output keeps the research archive available for applications. When updating an existing deployment, deploy the fresh export as a complete set so removed assets leave the site as well.

## License

The template is [MIT licensed](LICENSE). PDF generation uses [RenderCV](https://github.com/rendercv/rendercv). The website loads [Instrument Serif](https://github.com/google/fonts/tree/main/ofl/instrumentserif) and [Inter](https://github.com/google/fonts/tree/main/ofl/inter) via Google Fonts.
