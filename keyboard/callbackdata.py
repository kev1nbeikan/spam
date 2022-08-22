from aiogram.utils.callback_data import CallbackData
from data.strings import FilesUploadingStrings, SelMembershipStrings, AdminPanelStrings

check_sessions_data = CallbackData(FilesUploadingStrings.QUERY_CHECK_ACCS, 'folder')
buy_membership_data = CallbackData(SelMembershipStrings.QUERY_SELL, 'product_id')
check_paying_data = CallbackData(SelMembershipStrings.QUERY_PAY, 'bill_id', 'days')
change_msh_data = CallbackData(AdminPanelStrings.CHANGE_MS_QUERY, 'id_', 'cmd')
change_msg_data = CallbackData(AdminPanelStrings.CHANGE_MSG_QUERY, 'section')

connect_bot_data = CallbackData(AdminPanelStrings.CONNECT_BOT, 'file_name')
delete_bot_data = CallbackData(AdminPanelStrings.DELETE_BOT, 'file_name')