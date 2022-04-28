from sqlalchemy import func, column, Text, Boolean
from src.models.postgres import Thread

from src.bases.logic import Logic


class ThreadLogic(Logic):
    def find_thread(self):
        items = func.jsonb_to_recordset(Thread.messages).table_valued(
            column("folder", Text),
            column("id", Text)).render_derived(with_types=True)

        query = self.session.query(Thread).filter(
            items.c.folder == 'INBOX'
        ).distinct(Thread.id)
        for t in query:
            print(t.id, t.messages)
