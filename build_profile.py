from argparse import ArgumentParser
from pathlib import Path
import re
import shutil
import subprocess
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
from ruamel.yaml import YAML


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'build'
TEMPLATES = ROOT / 'site'
PUBLIC_CV_NAME = 'CV'
YAML = YAML(typ='safe')
YAML.sort_base_mapping_type_on_output = False


def load_projects():
    records = {}
    for path in sorted((ROOT / 'projects').glob('*.md')):
        parts = re.split(r'^---[ \t]*$', path.read_text(encoding='utf-8'), maxsplit=2, flags=re.MULTILINE)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'Expected YAML front matter in {path.name}')
        record = YAML.load(parts[1])
        project_id = record['id']
        if project_id != path.stem or project_id in records:
            raise ValueError(f'Invalid project id in {path.name}')
        records[project_id] = record
    return records


def cv_project(record, highlights):
    entry = {
        'name': record['title'],
        'start_date': record['start_date'],
        'highlights': highlights,
    }
    if record.get('end_date'):
        entry['end_date'] = record['end_date']
    else:
        entry.pop('start_date')
        entry['date'] = f"Started {record['start_date']}"
    return entry


def render_cv(filename, profile, projects, publications, is_public):
    education = dict(profile['education'])
    if is_public:
        education = {key: education[key] for key in (
            'institution', 'area', 'degree', 'date'
        )}
    sections = {
        'Education': [education],
        'Research Experience': projects,
        'Publications': [
            {
                'title': item['title'], 'authors': item['authors'],
                'journal': item['venue'],
                **({'url': item['url']} if item.get('url') else {}),
            }
            for item in publications
        ],
    }
    if not is_public:
        sections['Honors and Awards'] = [{'bullet': item} for item in profile.get('awards', [])]
        sections['Activities'] = [{'bullet': item} for item in profile.get('activities', [])]

    source = BUILD / f'{filename}.yml'
    with source.open('w', encoding='utf-8') as output:
        YAML.dump({
            'cv': {
                'name': profile['name'],
                **({'website': profile['website']} if profile.get('website') else {}),
                'sections': {title: entries for title, entries in sections.items() if entries},
            },
            'design': {'theme': 'classic'},
        }, output)
    pdf = BUILD / f'{filename}.pdf'
    typst = BUILD / f'{filename}.typ'
    pdf.unlink(missing_ok=True)
    subprocess.run([
        sys.executable, '-X', 'utf8', '-m', 'rendercv', 'render', str(source), '--quiet',
        '--output-folder', str(BUILD), '--pdf-path', str(pdf), '--typst-path', str(typst),
        '--dont-generate-markdown',
        '--dont-generate-html', '--dont-generate-png',
    ], check=True)
    if not pdf.is_file():
        raise RuntimeError(f'RenderCV did not create {pdf.name}')
    return pdf


def project_image(image):
    if not image:
        return None
    filename = image['file']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*\.(?:png|jpg|jpeg|webp)', filename):
        raise ValueError(f'Expected a raster image filename, got {filename!r}')
    asset_dir = TEMPLATES / 'assets'
    asset = asset_dir / filename
    if asset.resolve().parent != asset_dir.resolve() or not asset.is_file():
        raise ValueError(f'Image is missing from site/assets: {filename}')
    return {'file': filename, 'alt': image['alt'], 'caption': image.get('caption')}


def main():
    parser = ArgumentParser(description='Generate Master CV, public CV and the public site.')
    parser.add_argument('--site-output', type=Path, default=BUILD / 'public-site')
    args = parser.parse_args()
    profile = YAML.load(ROOT / 'profile.yml')
    projects = load_projects()
    publications = YAML.load(ROOT / 'publications.yml')
    selection = YAML.load(ROOT / 'cv' / 'selection.yml')
    public_publications = {key: publications[key] for key in selection['public_publications']}
    site_projects = []
    public_cv_projects = []
    for key in selection['public_projects']:
        project = projects[key]
        public = project['public']
        site_projects.append({
            'title': public['title'], 'summary': public['summary'],
            'publication': public_publications.get(public.get('publication')),
            'image': project_image(public.get('image')),
        })
        entry = cv_project(project, public['highlights'])
        entry['name'] = public['title']
        public_cv_projects.append(entry)

    master_projects = []
    for item in sorted(projects.values(), key=lambda item: item['start_date'], reverse=True):
        entry = cv_project(item, item['highlights'])
        if item.get('role'):
            entry['summary'] = item['role']
        master_projects.append(entry)

    BUILD.mkdir(exist_ok=True)
    render_cv(
        'Master_CV', profile, master_projects, publications.values(), is_public=False,
    )
    public_pdf = render_cv(
        PUBLIC_CV_NAME, profile, public_cv_projects, public_publications.values(), is_public=True,
    )

    site_output = args.site_output.resolve()
    site_output.mkdir(parents=True, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(),
        trim_blocks=True, lstrip_blocks=True,
    )
    html = env.get_template('index.html').render(
        name=profile['name'], affiliation=profile['affiliation'], bio=profile['bio'],
        website=profile.get('website'), github_url=profile.get('github_url'),
        example=profile.get('example', False), cv_filename=public_pdf.name,
        projects=site_projects, publications=public_publications.values(),
    )
    (site_output / 'index.html').write_text(html + '\n', encoding='utf-8', newline='\n')
    (site_output / '.nojekyll').touch()
    images = {project['image']['file'] for project in site_projects if project['image']}
    for filename in sorted(images | {'style.css'}):
        shutil.copyfile(TEMPLATES / 'assets' / filename, site_output / filename)
    shutil.copyfile(public_pdf, site_output / public_pdf.name)


if __name__ == '__main__':
    main()
