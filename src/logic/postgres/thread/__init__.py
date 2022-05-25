from sqlalchemy import func, column, Text, Boolean, String
from sqlalchemy.future import select

from src.models.postgres import Thread, Folder
from src.bases.logic import Logic


class ThreadLogic(Logic):
    def find_thread(self, folder=None):
        items = func.jsonb_to_recordset(Thread.messages).table_valued(
            column("folder", Text),
            column("id", Text)).render_derived(
            with_types=True
        )

        query = self.session.query(Thread).filter(
            items.c.folder == folder
        )
        return query

    def find_thread2(self, folder=None):
        items = func.jsonb_to_recordset(
            Thread.messages
        ).table_valued(
            column("folder", Text),
            column("id", Text)
        ).render_derived(
            with_types=True
        )

        query = select(Thread.id)
        if folder:
            query = query.where(items.c.folder == 'INBOX')

        return query

    def find_thread3(self, folder=None):
        return self.session.query(Thread).join(Folder, Thread.folders).filter(
            Folder.id == folder
        )