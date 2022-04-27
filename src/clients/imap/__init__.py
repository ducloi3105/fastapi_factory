from imap_tools import MailBox, MailMessage

from src.common.logging import log_data
from src.common.constants.imap import ImapConstants
from src.common.utils import generate_message_id
from src.bases.error.client import ClientError
from config import ImapConfig


class ImapClient:
    def __init__(self, email: str, password: str):
        self.imap_host = ImapConfig.imap_host
        self.imap_port = ImapConfig.imap_port
        self.email = email
        self.password = password
        self.client = self.init_client()
        self.login = self.connect()

    def init_client(self) -> MailBox:
        return MailBox(self.imap_host, self.imap_port, self.ssl)

    def connect(self):
        try:
            self.client.login(self.email, self.password)
        except Exception as e:
            log_data(
                mode='error',
                template='Could not login to imap server: {e}',
                kwargs=dict(e=e)
            )
            raise ClientError("Could not login to imap server")

    def list_folders(self, folder: str | None = None) -> list:
        params = dict()
        if folder is not None:
            params['folder'] = folder
        return self.client.folder.list(**params)
    
    def create_folder(self, folder: str):
        _, message = self.client.folder.create(folder=folder)
        if "Create completed" not in message:
            log_data(
                mode='error',
                template='Could not create folder: {folder}',
                kwargs=dict(folder=folder)
            )
            raise ClientError(message)

    def delete_folder(self, folder: str):
        _, message = self.client.folder.delete(folder=folder)
        if "Delete completed" not in message:
            log_data(
                mode='error',
                template='Could not delete folder: {folder}',
                kwargs=dict(folder=folder)
            )
            raise ClientError(message)

    def rename_folder(self, old_name: str, new_name: str):
        _, message = self.client.folder.rename(
            old_name=old_name,
            new_name=new_name
        )
        if "Rename completed" not in message:
            log_data(
                    mode='error',
                    template='Could not rename folder: {old_name}',
                    kwargs=dict(old_name=old_name)
                )
            raise ClientError(message)
    
    def set_flags(self, uids: list[int], flag: str):
        result, _ = self.client.flag(
            uid_list=uids,
            flag_set=flag,
            value=True
        )
        ok, message = result
        if "UID" not in message:
            log_data(
                    mode='error',
                    template='Could not set flag for uids: {uids}',
                    kwargs=dict(uids=uids)
                )
            raise ClientError(message)

    def delete_mesages(self, folder: str, uids: list[int]):
        self.client.folder.set(folder=folder)
        result, _= self.client.delete(uids)
        _, message = result
        if "Deleted" not in message:
            log_data(
                    mode='error',
                    template='Could not delete uids: {uids}, folder: {folder}',
                    kwargs=dict(uids=uids, folder=folder)
                )
            raise ClientError(message)

    def empty_folder(self, folder: str):
        self.client.folder.set(folder=folder)
        uids = self.client.uids()
        result, _ = self.client.delete(uids)
        _, message = result
        if "Deleted" not in message:
            log_data(
                    mode='error',
                    template='Could not empty folder: {folder}',
                    kwargs=dict(folder=folder)
                )
            raise ClientError(message)
    
    def new_message(self, folder: str, flags: list[str]) -> dict:
        uniq_id = generate_message_id(ImapConfig.message_id_prefix)
        message_id_header = ImapConstants.message_id_header.format(uniq_id)

        self.client.folder.set(folder=folder)
        message = MailMessage.from_bytes(bytes(message_id_header, 'utf-8'))
        _, message = self.client.append(
            folder=folder,
            flag_set=flags,
            message=message
        )
        if "Append completed" not in message:
            log_data(
                    mode='error',
                    template='Could not create new message - folder: {folder}',
                    kwargs=dict(folder=folder)
                )
            raise ClientError(message)

        response = self.client.fetch(
            ImapConstants.SEARCH_CRITERIA_BY_MESSAGE_HEADER_ID.format(uniq_id))
        uid = next(response).uid
        return dict(uid=uid, message_id_header=message_id_header)
