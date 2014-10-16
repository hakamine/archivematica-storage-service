# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import locations.models.space
from django.conf import settings
import django.core.validators
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(max_length=36, editable=False, blank=True)),
                ('uri', models.CharField(help_text=b'URL to contact upon callback execution.', max_length=1024)),
                ('event', models.CharField(help_text=b'Type of event when this callback should be executed.', max_length=15, choices=[(b'post_store', b'Post-store')])),
                ('method', models.CharField(help_text=b'HTTP request method to use in connecting to the URL.', max_length=10, choices=[(b'delete', b'DELETE'), (b'get', b'GET'), (b'head', b'HEAD'), (b'options', b'OPTIONS'), (b'patch', b'PATCH'), (b'post', b'POST'), (b'put', b'PUT')])),
                ('expected_status', models.IntegerField(default=200, help_text=b'Expected HTTP response from the server, used to validate the callback response.')),
                ('enabled', models.BooleanField(default=True, help_text=b'Enabled if this callback should be executed.')),
            ],
            options={
                'verbose_name': 'Callback',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Duracloud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(help_text=b'Hostname of the DuraCloud instance. Eg. trial.duracloud.org', max_length=256)),
                ('user', models.CharField(help_text=b'Username to authenticate as', max_length=64)),
                ('password', models.CharField(help_text=b'Password to authenticate with', max_length=64)),
                ('duraspace', models.CharField(help_text=b'Name of the Space within DuraCloud', max_length=64)),
            ],
            options={
                'verbose_name': 'DuraCloud',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(max_length=8, choices=[(b'DELETE', b'delete')])),
                ('event_reason', models.TextField()),
                ('user_id', models.PositiveIntegerField()),
                ('user_email', models.EmailField(max_length=254)),
                ('status', models.CharField(max_length=8, choices=[(b'SUBMIT', b'Submitted'), (b'APPROVE', b'Approved'), (b'REJECT', b'Rejected')])),
                ('status_reason', models.TextField(null=True, blank=True)),
                ('status_time', models.DateTimeField(auto_now=True)),
                ('store_data', models.TextField(null=True, editable=False, blank=True)),
                ('admin_id', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Event',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fedora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fedora_user', models.CharField(help_text=b'Fedora user name (for SWORD functionality)', max_length=64)),
                ('fedora_password', models.CharField(help_text=b'Fedora password (for SWORD functionality)', max_length=256)),
                ('fedora_name', models.CharField(help_text=b'Name or IP of the remote Fedora machine.', max_length=256)),
            ],
            options={
                'verbose_name': 'FEDORA',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(help_text=b'Unique identifier', unique=True, max_length=36, editable=False, blank=True)),
                ('name', models.TextField(max_length=1000)),
                ('source_id', models.TextField(max_length=128)),
                ('checksum', models.TextField(max_length=128)),
                ('stored', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Callback File',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalFilesystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Local Filesystem',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(help_text=b'Unique identifier', unique=True, max_length=36, editable=False, blank=True)),
                ('purpose', models.CharField(help_text=b'Purpose of the space.  Eg. AIP storage, Transfer source', max_length=2, choices=[(b'AS', b'AIP Storage'), (b'CP', b'Currently Processing'), (b'DS', b'DIP Storage'), (b'SD', b'FEDORA Deposits'), (b'SS', b'Storage Service Internal Processing'), (b'BL', b'Transfer Backlog'), (b'TS', b'Transfer Source')])),
                ('relative_path', models.TextField(help_text=b"Path to location, relative to the storage space's path.")),
                ('description', models.CharField(default=None, max_length=256, null=True, help_text=b'Human-readable description.', blank=True)),
                ('quota', models.BigIntegerField(default=None, help_text=b'Size, in bytes (optional)', null=True, blank=True)),
                ('used', models.BigIntegerField(default=0, help_text=b'Amount used, in bytes.')),
                ('enabled', models.BooleanField(default=True, help_text=b'True if space can be accessed.')),
            ],
            options={
                'verbose_name': 'Location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationPipeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.ForeignKey(to='locations.Location', to_field=b'uuid')),
            ],
            options={
                'verbose_name': 'Location associated with a Pipeline',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lockssomatic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('au_size', models.BigIntegerField(help_text=b'Size in bytes of an Allocation Unit', null=True, verbose_name=b'AU Size', blank=True)),
                ('sd_iri', models.URLField(help_text=b'URL of LOCKSS-o-matic service document IRI, eg. http://lockssomatic.example.org/api/sword/2.0/sd-iri', max_length=256, verbose_name=b'Service Document IRI')),
                ('collection_iri', models.CharField(help_text=b'URL to post the packages to, eg. http://lockssomatic.example.org/api/sword/2.0/col-iri/12', max_length=256, null=True, verbose_name=b'Collection IRI', blank=True)),
                ('content_provider_id', models.CharField(help_text=b'On-Behalf-Of value when communicating with LOCKSS-o-matic', max_length=32, verbose_name=b'Content Provider ID')),
                ('external_domain', models.URLField(help_text=b'Base URL for this server that LOCKSS will be able to access.  Probably the URL for the home page of the Storage Service.', verbose_name=b'Externally available domain')),
                ('checksum_type', models.CharField(help_text=b'Checksum type to send to LOCKSS-o-matic for verification.  Eg. md5, sha1, sha256', max_length=64, null=True, verbose_name=b'Checksum type', blank=True)),
                ('keep_local', models.BooleanField(default=True, help_text=b'If checked, keep a local copy even after the AIP is stored in the LOCKSS network.', verbose_name=b'Keep local copy?')),
            ],
            options={
                'verbose_name': 'LOCKSS-o-matic',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NFS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_name', models.CharField(help_text=b'Name of the NFS server.', max_length=256)),
                ('remote_path', models.TextField(help_text=b'Path on the NFS server to the export.')),
                ('version', models.CharField(default=b'nfs4', help_text=b'Type of the filesystem, i.e. nfs, or nfs4.         Should match a command in `mount`.', max_length=64)),
                ('manually_mounted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Network File System (NFS)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(help_text=b'Unique identifier', unique=True, max_length=36, editable=False, blank=True)),
                ('description', models.CharField(default=None, max_length=256, null=True, help_text=b'Human-readable description.', blank=True)),
                ('current_path', models.TextField()),
                ('pointer_file_path', models.TextField(null=True, blank=True)),
                ('size', models.IntegerField(default=0, help_text=b'Size in bytes of the package')),
                ('package_type', models.CharField(max_length=8, choices=[(b'AIP', b'AIP'), (b'AIC', b'AIC'), (b'SIP', b'SIP'), (b'DIP', b'DIP'), (b'transfer', b'Transfer'), (b'file', b'Single File'), (b'deposit', b'FEDORA Deposit')])),
                ('status', models.CharField(default=b'FAIL', help_text=b'Status of the package in the storage service.', max_length=8, choices=[(b'PENDING', b'Upload Pending'), (b'STAGING', b'Staged on Storage Service'), (b'UPLOADED', b'Uploaded'), (b'VERIFIED', b'Verified'), (b'FAIL', b'Failed'), (b'DEL_REQ', b'Delete requested'), (b'DELETED', b'Deleted'), (b'FINALIZE', b'Deposit Finalized')])),
                ('misc_attributes', jsonfield.fields.JSONField(default={}, help_text=b'For storing flexible, often Space-specific, attributes', null=True, blank=True)),
                ('current_location', models.ForeignKey(to='locations.Location', to_field=b'uuid')),
            ],
            options={
                'verbose_name': 'Package',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageDownloadTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(help_text=b'Unique identifier', unique=True, max_length=36, editable=False, blank=True)),
                ('downloads_attempted', models.IntegerField(default=0)),
                ('downloads_completed', models.IntegerField(default=0)),
                ('download_completion_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('package', models.ForeignKey(to='locations.Package', to_field=b'uuid')),
            ],
            options={
                'verbose_name': 'Package Download Task',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageDownloadTaskFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(help_text=b'Unique identifier', unique=True, max_length=36, editable=False, blank=True)),
                ('filename', models.CharField(max_length=256)),
                ('url', models.TextField()),
                ('completed', models.BooleanField(default=False, help_text=b'True if file downloaded successfully.')),
                ('failed', models.BooleanField(default=False, help_text=b'True if file failed to download.')),
                ('task', models.ForeignKey(related_name=b'download_file_set', to='locations.PackageDownloadTask', to_field=b'uuid')),
            ],
            options={
                'verbose_name': 'Package Download Task File',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(validators=[django.core.validators.RegexValidator(b'\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}', b'Needs to be format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx where x is a hexadecimal digit.', b'Invalid UUID')], editable=False, max_length=36, blank=True, help_text=b'Identifier for the Archivematica pipeline', unique=True, verbose_name=b'UUID')),
                ('description', models.CharField(default=None, max_length=256, null=True, help_text=b'Human readable description of the Archivematica instance.', blank=True)),
                ('remote_name', models.CharField(default=None, max_length=256, null=True, help_text=b'Host or IP address of the pipeline server for making API calls.', blank=True)),
                ('api_username', models.CharField(default=None, max_length=256, null=True, help_text=b'Username to use when making API calls to the pipeline.', blank=True)),
                ('api_key', models.CharField(default=None, max_length=256, null=True, help_text=b'API key to use when making API calls to the pipeline.', blank=True)),
                ('enabled', models.BooleanField(default=True, help_text=b'Enabled if this pipeline is able to access the storage service.')),
            ],
            options={
                'verbose_name': 'Pipeline',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PipelineLocalFS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_user', models.CharField(help_text=b'Username on the remote machine accessible via ssh', max_length=64)),
                ('remote_name', models.CharField(help_text=b'Name or IP of the remote machine.', max_length=256)),
            ],
            options={
                'verbose_name': 'Pipeline Local FS',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(help_text=b'Unique identifier', unique=True, max_length=36, editable=False, blank=True)),
                ('access_protocol', models.CharField(help_text=b'How the space can be accessed.', max_length=8, choices=[(b'DC', b'DuraCloud'), (b'FEDORA', b'FEDORA via SWORD2'), (b'FS', b'Local Filesystem'), (b'LOM', b'LOCKSS-o-matic'), (b'NFS', b'NFS'), (b'PIPE_FS', b'Pipeline Local Filesystem')])),
                ('size', models.BigIntegerField(default=None, help_text=b'Size in bytes (optional)', null=True, blank=True)),
                ('used', models.BigIntegerField(default=0, help_text=b'Amount used in bytes')),
                ('path', models.TextField(default=b'', help_text=b'Absolute path to the space on the storage service machine.', blank=True)),
                ('staging_path', models.TextField(help_text=b'Absolute path to a staging area.  Must be UNIX filesystem compatible, preferably on the same filesystem as the path.', validators=[locations.models.space.validate_space_path])),
                ('verified', models.BooleanField(default=False, help_text=b'Whether or not the space has been verified to be accessible.')),
                ('last_verified', models.DateTimeField(default=None, help_text=b'Time this location was last verified to be accessible.', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Space',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pipelinelocalfs',
            name='space',
            field=models.OneToOneField(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='package',
            name='origin_pipeline',
            field=models.ForeignKey(to_field=b'uuid', blank=True, to='locations.Pipeline', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='package',
            name='pointer_file_location',
            field=models.ForeignKey(related_name=b'+', to_field=b'uuid', blank=True, to='locations.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nfs',
            name='space',
            field=models.OneToOneField(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lockssomatic',
            name='space',
            field=models.OneToOneField(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locationpipeline',
            name='pipeline',
            field=models.ForeignKey(to='locations.Pipeline', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='pipeline',
            field=models.ManyToManyField(help_text=b'UUID of the Archivematica instance using this location.', to='locations.Pipeline', null=True, through='locations.LocationPipeline', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='space',
            field=models.ForeignKey(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localfilesystem',
            name='space',
            field=models.OneToOneField(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fedora',
            name='space',
            field=models.OneToOneField(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='package',
            field=models.ForeignKey(to='locations.Package', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='pipeline',
            field=models.ForeignKey(to='locations.Pipeline', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duracloud',
            name='space',
            field=models.OneToOneField(to='locations.Space', to_field=b'uuid'),
            preserve_default=True,
        ),
    ]
