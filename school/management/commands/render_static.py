from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Render selected templates to static HTML files for static hosting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', '-o', dest='output', default='dist/public', help='Output directory'
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output'])
        templates_dir = Path(settings.BASE_DIR) / 'school' / 'templates' / 'school'
        output_dir.mkdir(parents=True, exist_ok=True)

        mapping = {
            'home.html': 'index.html',
        }

        for tpl in sorted(templates_dir.glob('*.html')):
            tpl_name = tpl.name
            out_name = mapping.get(tpl_name, tpl_name)
            try:
                rendered = render_to_string(f'school/{tpl_name}', {})
            except Exception as e:
                self.stderr.write(f'Error rendering {tpl_name}: {e}')
                continue

            out_path = output_dir / out_name
            out_path.write_text(rendered, encoding='utf-8')
            self.stdout.write(f'Wrote {out_path}')

        self.stdout.write(self.style.SUCCESS(f'Rendered templates to {output_dir}'))
