import win32com.client as win32
path = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\AlkekSensourceData"
outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
#get all messages in this folder
messages = inbox.Items
#messages.sort("[ReceivedTime")

#check messages exist
if len(messages) == 0:
    print("No messages in Inbox")
    exit()

#loop through all messages.
emails = []
for message in messages:
    if message.subject.startswith("Alkek doorcount by hour"):
        this_message = (
            message.Subject,
            message.SenderEmailAddress,
            message.Attachments
        )

        emails.append(this_message)

#show results:
for email in emails:
    #unpack the tuple to get at info
    subject, from_address, attachments = email
    for attachment in attachments:
        attachment.SaveAsFile(path + "/" + subject + ".csv")
print("Saved {0} attachments".format(len(emails)))
#print(emails)