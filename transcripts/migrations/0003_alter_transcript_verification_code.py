from django.db import migrations, models
import secrets


def generate_verification_code():

    return (
        "WRU-TR-"
        f"{secrets.token_hex(6).upper()}"
    )


def populate_verification_codes(
    apps,
    schema_editor
):

    Transcript = apps.get_model(
        "transcripts",
        "Transcript"
    )

    used_codes = set()

    for transcript in Transcript.objects.all():

        while True:

            code = generate_verification_code()

            if code not in used_codes:

                used_codes.add(code)

                break

        transcript.verification_code = code

        transcript.save(
            update_fields=[
                "verification_code"
            ]
        )


class Migration(migrations.Migration):

    dependencies = [

        (
            "transcripts",
            "0002_alter_transcript_verification_code"
        ),

    ]

    operations = [

        migrations.AlterField(

            model_name="transcript",

            name="verification_code",

            field=models.CharField(

                blank=True,

                editable=False,

                max_length=30,

                null=True

            ),

        ),

        migrations.RunPython(

            populate_verification_codes,

            migrations.RunPython.noop

        ),

        migrations.AlterField(

            model_name="transcript",

            name="verification_code",

            field=models.CharField(

                editable=False,

                max_length=30,

                unique=True

            ),

        ),

    ]