from imap_tools import MailMessageFlags

class ImapFlag(MailMessageFlags):
    FLAGS = 'FLAGS'
    BODY = 'BODY[]'
    MESSAGE_ID = 'BODY[HEADER.FIELDS (MESSAGE-ID)]'
    INTERNALDATE = 'INTERNALDATE'
    MOVED = '$Moved'
    DRAFT_FROM_WEBMAIL = '$DRAFT_FROM_WEBMAIL'
    SENT_FROM_WEBMAIL = '$SENT_FROM_WEBMAIL'
    SEARCH_CRITERIA_BY_MESSAGE_HEADER_ID = 'HEADER "Message-ID" "{}"'
    FIELDS = [
        FLAGS,
        BODY,
        INTERNALDATE,
    ]
