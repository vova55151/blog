from django.test import TestCase


class TestOtherFiles(TestCase):
    # def test_settings_import_error(self):
    #     with self.assertRaises(ImportError):  # TODO: ?
    #         pass

    def test_celery_debug_task(self):
        from blg.celery import debug_task
        self.assertIsNone(debug_task())

