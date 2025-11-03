import mailtrap as mt

mail = mt.Mail(
    sender=mt.Address(email="contact@sengleongaircond.com.my", name="Mailtrap Test"),
    to=[mt.Address(email="karimazizc@gmail.com")],
    subject="You are awesome!",
    text="Congrats for sending test email with Mailtrap!",
    category="Integration Test",
)

client = mt.MailtrapClient(token="1a9a463f9de02873dbfc294503cb2b94")
response = client.send(mail)

print(response)
