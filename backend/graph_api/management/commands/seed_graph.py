from django.core.management.base import BaseCommand

from graph_api.seed import seed_database


class Command(BaseCommand):
    help = "Seed CognoDB with SkillConnect graph data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding SkillConnect graph...")

        try:
            seed_database()

            self.stdout.write(
                self.style.SUCCESS(
                    "SkillConnect graph seeded successfully!"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error while seeding database: {e}"
                )
            )