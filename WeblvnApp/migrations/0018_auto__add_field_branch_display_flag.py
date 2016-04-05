# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Branch.display_flag'
        db.add_column('WeblvnApp_branch', 'display_flag', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Branch.display_flag'
        db.delete_column('WeblvnApp_branch', 'display_flag')


    models = {
        'WeblvnApp.branch': {
            'Meta': {'ordering': "['branch_name']", 'object_name': 'Branch'},
            'bfr_id': ('django.db.models.fields.IntegerField', [], {}),
            'branch_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'display_flag': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'WeblvnApp.build_entry': {
            'Meta': {'object_name': 'Build_entry'},
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'build': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'build_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rel': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'rev': ('django.db.models.fields.IntegerField', [], {})
        },
        'WeblvnApp.dbupdate': {
            'Meta': {'object_name': 'DBUpdate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdDate': ('django.db.models.fields.DateTimeField', [], {})
        },
        'WeblvnApp.isu_working_path': {
            'Meta': {'object_name': 'ISU_working_path'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'otherInfo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'result_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'src_branch_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'src_branch_name'", 'to_field': "'branch_name'", 'to': "orm['WeblvnApp.Branch']"}),
            'src_build_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'src_iso': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'success': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '4'}),
            'test_date': ('django.db.models.fields.DateField', [], {}),
            'tester': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trg_branch_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trg_branch_name'", 'to_field': "'branch_name'", 'to': "orm['WeblvnApp.Branch']"}),
            'trg_build_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'trg_iso': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type_of': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'WeblvnApp.kbentry': {
            'Meta': {'object_name': 'KBEntry'},
            'brief_desc': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'det_desc': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'WeblvnApp.lvn_entry': {
            'Meta': {'object_name': 'Lvn_entry'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'commit_date': ('django.db.models.fields.DateTimeField', [], {}),
            'h_file_change': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inc_file_change': ('django.db.models.fields.IntegerField', [], {}),
            'layout_check': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'layout_done': ('django.db.models.fields.IntegerField', [], {}),
            'layout_rev': ('django.db.models.fields.IntegerField', [], {}),
            'layout_status': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'lvn': ('django.db.models.fields.IntegerField', [], {}),
            'md5sum_str': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'src_dir_change': ('django.db.models.fields.IntegerField', [], {})
        },
        'WeblvnApp.lvn_feature_related': {
            'Meta': {'object_name': 'LVN_Feature_Related'},
            'affected_structures': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lvn': ('django.db.models.fields.IntegerField', [], {}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'title': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        },
        'WeblvnApp.uploaded_files': {
            'Meta': {'object_name': 'Uploaded_Files'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'WeblvnApp.wiki_entry': {
            'Meta': {'object_name': 'Wiki_entry'},
            'adaptation': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'bfr_lvn': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'branch_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['WeblvnApp.Branch']", 'to_field': "'branch_name'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'rev_id': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['WeblvnApp']
