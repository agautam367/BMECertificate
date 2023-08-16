# import google_workspace
#
# service = google_workspace.service.GoogleService(
#     api="gmail",
#     session="my-gmail",
#     client_secrets="/Users/aarushigautam6/Desktop/HCI/Output/Output-CV"
#     )
# service.local_oauth()
#
# gmail_client = google_workspace.gmail.GmailClient(service=service)
# print(gmail_client.email_address)
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import google_workspace
from googleapiclient.discovery import build
from google_workspace.service import GoogleService
import base64
# Get the current date
current_date = datetime.today().date()
print(current_date)


# def sendmail(template_path, font_path):
#     service = google_workspace.service.GoogleService(
#         api="gmail",
#         session="my-gmail",
#         client_secrets="/Users/aarushigautam6/Desktop/HCI/Output/Output-CV/client_secret.json"
#     )
#     service.local_oauth()
#
#     gmail_client = google_workspace.gmail.GmailClient(service=service)
#     print(gmail_client.email_address)
#
#     unread_messages = [message for message in gmail_client.get_messages("inbox") if message.is_unread()]
#
#
#     for message in unread_messages:
#         if(message.subject=="Congratulations on your course completion"):
#             print(message.from_)
#             message.mark_read()
#             # message.reply("Hi!")
#             output_path = f"/Users/aarushigautam6/Desktop/HCI/Output/Output-CV/{message.from_}_certificate.png"
#             create_certificate(message.from_, template_path, font_path, output_path)
#             print(f"Certificate for {message.from_} created: {output_path}")
#             sent_message = gmail_client.send_message(
#             to=message.from_,
#             # cc=["aarushi@brightmindenrichment.org","akshayd@brightmindenrichment.org","jiani@brightmindenrichment.org"],
#             subject="Certifcate testing!",
#             html="<b>HTML here</b>",
#             attachments=[output_path]
#                 )

def sendmail(template_path, font_path):
    service = GoogleService(api="gmail", session="my-gmail", client_secrets="/path/to/client_secret.json")
    service.local_oauth()

    gmail_service = build("gmail", "v1", credentials=service.credentials)

    results = gmail_service.users().messages().list(userId="me", labelIds=["INBOX", "UNREAD"]).execute()
    messages = results.get("messages", [])
    gmail_client = google_workspace.gmail.GmailClient(service=service)
    print(gmail_client.email_address)

    for message in messages:
        msg = gmail_service.users().messages().get(userId="me", id=message["id"]).execute()
        headers = msg["payload"]["headers"]
        subject = [header["value"] for header in headers if header["name"] == "Subject"][0]

        if subject == "Congratulations on your course completion":
            from_email = [header["value"] for header in headers if header["name"] == "From"][0]
            from_email = from_email.replace(">", "").split("<")[1]

            output_path = f"/Users/aarushigautam6/Desktop/HCI/Output/Output-CV/{from_email}_certificate.png"
            create_certificate(from_email, template_path, font_path, output_path)
            print(f"Certificate for {from_email} created: {output_path}")
            sent_message = gmail_client.send_message(
                         to=from_email,
                        # cc=["aarushi@brightmindenrichment.org","akshayd@brightmindenrichment.org","jiani@brightmindenrichment.org"],
                         subject="Certifcate testing!",
                         html="<b>HTML here</b>",
                         attachments=[output_path]
                            )
            modify_request = {"removeLabelIds": ["UNREAD"]}
            gmail_service.users().messages().modify(userId="me", id=message["id"], body=modify_request).execute()
            # You can also send the email with the attachment here
def create_certificate(name, template_path, font_path, output_path):
    # Open the template image
    template = Image.open(template_path)

    # Create a drawing context
    draw = ImageDraw.Draw(template)

    # Load a font
    font = ImageFont.truetype(font_path, size=80)

    # Calculate text size and position
    text1 = f"{name}"
    text_width, text_height = draw.textsize(text1, font=font)
    position = ((template.width - text_width) // 2, (template.height - text_height) // 2.45)

    # Draw the text on the template
    draw.text(position, text1, fill=(0, 0, 0), font=font)

    text2 = str(current_date)
    text_width2, text_height2 = draw.textsize(text2, font=font)
    position2 = ((template.width - text_width2) //1.25, (template.height - text_height2) //1.2)

    # Draw the text on the template
    draw.text(position2, text2, fill=(0, 0, 0), font=font)

    # Save the customized certificate
    template.save(output_path)



if __name__ == "__main__":
    # Path to the certificate template image
    template_path = "/Users/aarushigautam6/Desktop/HCI/Output/Output-CV/Certificate1.png"

    # Path to the font file
    font_path = "/System/Library/Fonts/Supplemental/Apple Chancery.ttf"

    sendmail(template_path,font_path)
    # List of names
    # names = ["John Doe"]

    # for name in names:
    #     output_path = f"/Users/aarushigautam6/Desktop/HCI/Output/Output-CV/{name}_certificate.png"
    #     create_certificate(name, template_path, font_path, output_path)
    #     print(f"Certificate for {name} created: {output_path}")
